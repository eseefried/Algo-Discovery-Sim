"""Transactional local ledger. Money is integer virtual cents, never provider dollars."""

import hashlib
import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from uuid import uuid4

from .models import PREREQUISITES, REQUIREMENTS


def encoded(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)


class LeaseLost(RuntimeError):
    pass


class BudgetExhausted(RuntimeError):
    pass


class Ledger:
    def __init__(self, path: str | Path, *, clock=time.time):
        self.path = Path(path)
        self.clock = clock

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connection() as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.executescript("""
            CREATE TABLE IF NOT EXISTS roots (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, reward INTEGER NOT NULL,
                max_calls INTEGER NOT NULL, max_attempts INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'open', error TEXT, created REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY, genotype TEXT NOT NULL, parent_id TEXT,
                status TEXT NOT NULL, balance INTEGER NOT NULL, reserved INTEGER NOT NULL DEFAULT 0,
                heartbeat REAL NOT NULL, created REAL NOT NULL, ready INTEGER NOT NULL DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY, root_id TEXT NOT NULL REFERENCES roots(id),
                parent_id TEXT REFERENCES tasks(id), requirements TEXT NOT NULL,
                reward INTEGER NOT NULL, status TEXT NOT NULL DEFAULT 'Open',
                agent_id TEXT, token TEXT, lease_until REAL, auction_until REAL,
                round INTEGER NOT NULL DEFAULT 0, attempts INTEGER NOT NULL DEFAULT 0,
                result TEXT, created REAL NOT NULL, updated REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS bids (
                task_id TEXT NOT NULL, round INTEGER NOT NULL, agent_id TEXT NOT NULL,
                amount INTEGER NOT NULL, confidence REAL NOT NULL, status TEXT NOT NULL,
                PRIMARY KEY(task_id, round, agent_id)
            );
            CREATE TABLE IF NOT EXISTS wallets (
                id INTEGER PRIMARY KEY, agent_id TEXT NOT NULL, task_id TEXT,
                kind TEXT NOT NULL, delta INTEGER NOT NULL, created REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS calls (
                id TEXT PRIMARY KEY, root_id TEXT NOT NULL, task_id TEXT NOT NULL,
                agent_id TEXT NOT NULL, model TEXT NOT NULL, status TEXT NOT NULL,
                input_tokens INTEGER NOT NULL DEFAULT 0, output_tokens INTEGER NOT NULL DEFAULT 0,
                elapsed REAL NOT NULL DEFAULT 0, usage_known INTEGER NOT NULL DEFAULT 0, created REAL NOT NULL
            );
            CREATE TABLE IF NOT EXISTS events (
                seq INTEGER PRIMARY KEY, created REAL NOT NULL, actor TEXT NOT NULL,
                task_id TEXT, kind TEXT NOT NULL, data TEXT NOT NULL,
                previous_hash TEXT NOT NULL, hash TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS supervisor (
                singleton INTEGER PRIMARY KEY CHECK(singleton=1), owner TEXT NOT NULL,
                lease_until REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS tasks_root ON tasks(root_id, status);
            CREATE INDEX IF NOT EXISTS tasks_agent ON tasks(agent_id, status);
            """)

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=15, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=15000")
        try:
            yield db
        finally:
            db.close()

    @contextmanager
    def transaction(self):
        with self.connection() as db:
            db.execute("BEGIN IMMEDIATE")
            try:
                yield db
                db.execute("COMMIT")
            except BaseException:
                db.execute("ROLLBACK")
                raise

    def event(self, db, kind, actor, task_id=None, **data):
        row = db.execute("SELECT hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
        previous = row[0] if row else "0" * 64
        now, payload = self.clock(), encoded(data)
        digest = hashlib.sha256(
            encoded([now, actor, task_id, kind, payload, previous]).encode()
        ).hexdigest()
        db.execute(
            "INSERT INTO events(created,actor,task_id,kind,data,previous_hash,hash) VALUES(?,?,?,?,?,?,?)",
            (now, actor, task_id, kind, payload, previous, digest),
        )

    def wallet(self, db, agent_id, delta, kind, task_id=None):
        db.execute("UPDATE agents SET balance=balance+? WHERE id=?", (delta, agent_id))
        db.execute(
            "INSERT INTO wallets(agent_id,task_id,kind,delta,created) VALUES(?,?,?,?,?)",
            (agent_id, task_id, kind, delta, self.clock()),
        )
        self.event(db, "wallet", agent_id, task_id, delta=delta, category=kind)

    def submit(self, payload: dict, *, reward=50000, max_calls=12, max_attempts=3) -> str:
        if type(reward) is not int or reward < len(REQUIREMENTS) or not 1 <= max_calls <= 100:
            raise ValueError("Invalid reward or model-call budget.")
        if not 1 <= max_attempts <= 10:
            raise ValueError("Attempts must be between 1 and 10.")
        root = str(uuid4())
        with self.transaction() as db:
            db.execute(
                "INSERT INTO roots(id,payload,reward,max_calls,max_attempts,created) VALUES(?,?,?,?,?,?)",
                (root, encoded(payload), reward, max_calls, max_attempts, self.clock()),
            )
            db.execute(
                "INSERT INTO tasks(id,root_id,requirements,reward,created,updated) VALUES(?,?,?,?,?,?)",
                (root, root, encoded(REQUIREMENTS), reward, self.clock(), self.clock()),
            )
            self.event(db, "root_posted", "user", root, reward=reward, max_calls=max_calls)
        return root

    def create_agent(self, genotype: dict, *, parent_id=None, capital=10000) -> str:
        if type(capital) is not int or capital < 1:
            raise ValueError("Starting capital must be positive virtual cents.")
        with self.transaction() as db:
            number = db.execute("SELECT COUNT(*) FROM agents").fetchone()[0] + 1
            agent_id = f"agent-{number:04d}"
            db.execute(
                "INSERT INTO agents(id,genotype,parent_id,status,balance,heartbeat,created) VALUES(?,?,?,'active',0,?,?)",
                (agent_id, encoded(genotype), parent_id, self.clock(), self.clock()),
            )
            self.wallet(db, agent_id, capital, "endowment")
            self.event(
                db,
                "agent_spawned",
                "spawner",
                parent_id=parent_id,
                agent_id=agent_id,
                genotype=genotype,
            )
        return agent_id

    def agents(self, status=None):
        with self.connection() as db:
            sql = (
                "SELECT * FROM agents"
                + (" WHERE status=?" if status else "")
                + " ORDER BY created,id"
            )
            return [dict(row) for row in db.execute(sql, (status,) if status else ())]

    def root(self, root_id):
        with self.connection() as db:
            row = db.execute("SELECT * FROM roots WHERE id=?", (root_id,)).fetchone()
            if row is None:
                raise ValueError("Unknown root task.")
            return dict(row)

    def tasks(self, root_id):
        with self.connection() as db:
            return [
                dict(row)
                for row in db.execute(
                    "SELECT * FROM tasks WHERE root_id=? ORDER BY created,id", (root_id,)
                )
            ]

    @staticmethod
    def done_parts(db, root_id):
        return {
            part
            for row in db.execute(
                "SELECT result FROM tasks WHERE root_id=? AND status='Completed'", (root_id,)
            )
            for part in json.loads(row[0])["completed_requirements"]
        }

    def open_tasks(self):
        with self.connection() as db:
            ready = []
            for row in db.execute(
                "SELECT t.* FROM tasks t JOIN roots r ON r.id=t.root_id WHERE t.status='Open' AND r.status='open' ORDER BY t.reward DESC,t.created,t.id"
            ):
                parts = set(json.loads(row["requirements"]))
                completed = self.done_parts(db, row["root_id"])
                needed = set().union(*(PREREQUISITES[p] for p in parts)) - parts
                if needed <= completed:
                    ready.append(dict(row))
            return ready

    def bid(self, task_id, agent_id, amount, confidence, *, auction_seconds=1.0):
        if type(amount) is not int or amount < 1 or not 0 < confidence <= 1 or auction_seconds < 0:
            raise ValueError("Invalid bid.")
        with self.transaction() as db:
            task = db.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            agent = db.execute("SELECT * FROM agents WHERE id=?", (agent_id,)).fetchone()
            if not task or not agent or task["status"] != "Open" or agent["status"] != "active":
                return False
            if task["auction_until"] is not None and self.clock() >= task["auction_until"]:
                return False
            if db.execute(
                "SELECT 1 FROM bids WHERE task_id=? AND round=? AND agent_id=?",
                (task_id, task["round"], agent_id),
            ).fetchone():
                return False
            if amount > agent["balance"] - agent["reserved"]:
                return False
            db.execute("UPDATE agents SET reserved=reserved+? WHERE id=?", (amount, agent_id))
            db.execute(
                "INSERT INTO bids VALUES(?,?,?,?,?,'pending')",
                (task_id, task["round"], agent_id, amount, confidence),
            )
            db.execute(
                "UPDATE tasks SET auction_until=COALESCE(auction_until,?) WHERE id=?",
                (self.clock() + auction_seconds, task_id),
            )
            self.event(
                db,
                "bid_placed",
                agent_id,
                task_id,
                amount=amount,
                confidence=confidence,
                round=task["round"],
            )
            return True

    def release_bids(self, db, task):
        rows = db.execute(
            "SELECT * FROM bids WHERE task_id=? AND round=? AND status='pending'",
            (task["id"], task["round"]),
        ).fetchall()
        for bid in rows:
            db.execute(
                "UPDATE agents SET reserved=reserved-? WHERE id=?", (bid["amount"], bid["agent_id"])
            )
        db.execute(
            "UPDATE bids SET status='lost' WHERE task_id=? AND round=? AND status='pending'",
            (task["id"], task["round"]),
        )

    def award_due(self, *, lease_seconds=30):
        with self.transaction() as db:
            tasks = db.execute(
                "SELECT t.* FROM tasks t JOIN roots r ON r.id=t.root_id WHERE t.status='Open' AND r.status='open' AND t.auction_until<=?",
                (self.clock(),),
            ).fetchall()
            for task in tasks:
                winner = db.execute(
                    "SELECT b.* FROM bids b JOIN agents a ON a.id=b.agent_id WHERE b.task_id=? AND b.round=? AND b.status='pending' AND a.status='active' AND a.balance>=b.amount ORDER BY b.amount DESC,b.confidence DESC,b.agent_id LIMIT 1",
                    (task["id"], task["round"]),
                ).fetchone()
                self.release_bids(db, task)
                if winner is None:
                    db.execute(
                        "UPDATE tasks SET auction_until=NULL,round=round+1 WHERE id=?",
                        (task["id"],),
                    )
                    continue
                token = str(uuid4())
                db.execute(
                    "UPDATE bids SET status='won' WHERE task_id=? AND round=? AND agent_id=?",
                    (task["id"], task["round"], winner["agent_id"]),
                )
                self.wallet(db, winner["agent_id"], -winner["amount"], "winning_bid", task["id"])
                db.execute(
                    "UPDATE tasks SET status='Assigned',agent_id=?,token=?,lease_until=?,attempts=attempts+1,updated=? WHERE id=?",
                    (
                        winner["agent_id"],
                        token,
                        self.clock() + lease_seconds,
                        self.clock(),
                        task["id"],
                    ),
                )
                self.event(
                    db,
                    "task_awarded",
                    winner["agent_id"],
                    task["id"],
                    token=token,
                    amount=winner["amount"],
                )

    def assignment(self, agent_id):
        with self.connection() as db:
            row = db.execute(
                "SELECT * FROM tasks WHERE agent_id=? AND status='Assigned'", (agent_id,)
            ).fetchone()
            return dict(row) if row else None

    def heartbeat(self, agent_id, *, lease_seconds=30):
        with self.transaction() as db:
            now = self.clock()
            db.execute(
                "UPDATE agents SET heartbeat=?,ready=1 WHERE id=? AND status='active'",
                (now, agent_id),
            )
            # Expired contracts cannot be revived by a late heartbeat.
            db.execute(
                "UPDATE tasks SET lease_until=? WHERE agent_id=? AND status='Assigned' AND lease_until>? AND EXISTS(SELECT 1 FROM agents WHERE id=? AND status='active')",
                (now + lease_seconds, agent_id, now, agent_id),
            )

    def owned(self, db, task_id, agent_id, token):
        row = db.execute(
            "SELECT t.* FROM tasks t JOIN agents a ON a.id=t.agent_id JOIN roots r ON r.id=t.root_id WHERE t.id=? AND t.status='Assigned' AND t.agent_id=? AND t.token=? AND t.lease_until>? AND a.status='active' AND r.status='open'",
            (task_id, agent_id, token, self.clock()),
        ).fetchone()
        if row is None:
            raise LeaseLost("Task lease was revoked or expired.")
        return row

    def complete(self, task_id, agent_id, token, result: dict):
        with self.transaction() as db:
            task = self.owned(db, task_id, agent_id, token)
            parts = json.loads(task["requirements"])
            solved, groups = result["completed_requirements"], result["child_groups"]
            genotype = json.loads(
                db.execute("SELECT genotype FROM agents WHERE id=?", (agent_id,)).fetchone()[0]
            )
            if len(solved) > genotype["max_parts"]:
                raise ValueError("Contribution exceeds the agent's progress limit.")
            remaining = [part for part in parts if part not in solved]
            children = [part for group in groups for part in group]
            if not solved or len(solved) != len(set(solved)) or not set(solved) <= set(parts):
                raise ValueError("A contribution must complete a nonempty subset of its contract.")
            if any(not group for group in groups) or sorted(children) != sorted(remaining):
                raise ValueError("Child tasks must partition all remaining work exactly once.")
            previous = self.done_parts(db, task["root_id"])
            if any(not PREREQUISITES[part] <= previous | set(solved) for part in solved):
                raise ValueError("Contribution skipped prerequisite work.")
            own_reward = (
                task["reward"] if not remaining else task["reward"] * len(solved) // len(parts)
            )
            pool, count = task["reward"] - own_reward, len(remaining)
            for index, group in enumerate(groups):
                amount = pool if index == len(groups) - 1 else pool * len(group) // count
                child = str(uuid4())
                db.execute(
                    "INSERT INTO tasks(id,root_id,parent_id,requirements,reward,created,updated) VALUES(?,?,?,?,?,?,?)",
                    (
                        child,
                        task["root_id"],
                        task_id,
                        encoded(group),
                        amount,
                        self.clock(),
                        self.clock(),
                    ),
                )
                self.event(
                    db,
                    "child_posted",
                    agent_id,
                    child,
                    parent_id=task_id,
                    reward=amount,
                    requirements=group,
                )
                pool -= amount
                count -= len(group)
            db.execute(
                "UPDATE tasks SET status='Completed',result=?,lease_until=NULL,updated=? WHERE id=?",
                (encoded(result), self.clock(), task_id),
            )
            self.wallet(db, agent_id, own_reward, "reward", task_id)
            self.event(db, "portion_completed", agent_id, task_id, solved=solved, payout=own_reward)
            unfinished = db.execute(
                "SELECT COUNT(*) FROM tasks WHERE root_id=? AND status!='Completed'",
                (task["root_id"],),
            ).fetchone()[0]
            if not unfinished:
                db.execute("UPDATE roots SET status='completed' WHERE id=?", (task["root_id"],))
                self.event(db, "tree_completed", "ledger", task["root_id"])

    def reserve_call(self, task_id, agent_id, token, model):
        with self.transaction() as db:
            task = self.owned(db, task_id, agent_id, token)
            root = db.execute("SELECT * FROM roots WHERE id=?", (task["root_id"],)).fetchone()
            used = db.execute(
                "SELECT COUNT(*) FROM calls WHERE root_id=?", (root["id"],)
            ).fetchone()[0]
            if used >= root["max_calls"]:
                raise BudgetExhausted("Root model-call budget exhausted.")
            call_id = str(uuid4())
            db.execute(
                "INSERT INTO calls(id,root_id,task_id,agent_id,model,status,created) VALUES(?,?,?,?,?,'started',?)",
                (call_id, root["id"], task_id, agent_id, model, self.clock()),
            )
            self.event(db, "model_call_started", agent_id, task_id, call_id=call_id, model=model)
            return call_id

    def finish_call(self, call_id, *, status, input_tokens=None, output_tokens=None, elapsed=None):
        with self.transaction() as db:
            db.execute(
                "UPDATE calls SET status=?,input_tokens=COALESCE(?,input_tokens),output_tokens=COALESCE(?,output_tokens),elapsed=COALESCE(?,elapsed),usage_known=MAX(usage_known,?) WHERE id=?",
                (
                    status,
                    input_tokens,
                    output_tokens,
                    elapsed,
                    int(input_tokens is not None),
                    call_id,
                ),
            )

    def kill_agent(self, db, agent_id, reason):
        agent = db.execute("SELECT * FROM agents WHERE id=?", (agent_id,)).fetchone()
        if not agent or agent["status"] != "active":
            return
        for bid in db.execute(
            "SELECT * FROM bids WHERE agent_id=? AND status='pending'", (agent_id,)
        ).fetchall():
            db.execute(
                "UPDATE agents SET reserved=reserved-? WHERE id=?", (bid["amount"], agent_id)
            )
        db.execute(
            "UPDATE bids SET status='revoked' WHERE agent_id=? AND status='pending'", (agent_id,)
        )
        self.wallet(db, agent_id, -agent["balance"], "failure_burn")
        db.execute("UPDATE agents SET status='dead' WHERE id=?", (agent_id,))
        self.event(db, "agent_died", "spawner", agent_id=agent_id, reason=reason)

    def requeue(self, db, task, reason):
        root = db.execute("SELECT * FROM roots WHERE id=?", (task["root_id"],)).fetchone()
        if root["status"] != "open":
            db.execute(
                "UPDATE tasks SET status='Failed',lease_until=NULL,updated=? WHERE id=?",
                (self.clock(), task["id"]),
            )
        elif task["attempts"] >= root["max_attempts"]:
            self.close_root(db, root["id"], reason)
        else:
            db.execute(
                "UPDATE tasks SET status='Open',agent_id=NULL,token=NULL,lease_until=NULL,auction_until=NULL,round=round+1,updated=? WHERE id=?",
                (self.clock(), task["id"]),
            )
        self.event(db, "lease_revoked", "ledger", task["id"], reason=reason)

    def fail(self, task_id, agent_id, token, reason):
        with self.transaction() as db:
            task = self.owned(db, task_id, agent_id, token)
            self.kill_agent(db, agent_id, reason)
            self.requeue(db, task, reason)

    def reap(self, *, lease_seconds=30):
        with self.transaction() as db:
            for task in db.execute(
                "SELECT * FROM tasks WHERE status='Assigned' AND lease_until<=?", (self.clock(),)
            ).fetchall():
                self.kill_agent(db, task["agent_id"], "heartbeat expired")
                self.requeue(db, task, "heartbeat expired")
            for agent in db.execute(
                "SELECT id FROM agents WHERE status='active' AND ((ready=1 AND heartbeat<=?) OR (ready=0 AND created<=?) OR balance=0)",
                (self.clock() - lease_seconds, self.clock() - 60),
            ).fetchall():
                self.kill_agent(db, agent["id"], "worker heartbeat expired or wallet empty")

    def mark_crashed(self, agent_id):
        with self.transaction() as db:
            self.kill_agent(db, agent_id, "process exited unexpectedly; lease awaits expiry")

    def stop_agent(self, agent_id):
        with self.transaction() as db:
            for task in db.execute(
                "SELECT * FROM tasks WHERE status='Assigned' AND agent_id=?", (agent_id,)
            ).fetchall():
                self.requeue(db, task, "supervisor stopped")
            for bid in db.execute(
                "SELECT * FROM bids WHERE agent_id=? AND status='pending'", (agent_id,)
            ).fetchall():
                db.execute(
                    "UPDATE agents SET reserved=reserved-? WHERE id=?", (bid["amount"], agent_id)
                )
            db.execute(
                "UPDATE bids SET status='revoked' WHERE agent_id=? AND status='pending'",
                (agent_id,),
            )
            changed = db.execute(
                "UPDATE agents SET status='stopped' WHERE id=? AND status='active'", (agent_id,)
            )
            if changed.rowcount:
                self.event(db, "agent_stopped", "spawner", agent_id=agent_id)

    def fail_root(self, root_id, reason):
        with self.transaction() as db:
            self.close_root(db, root_id, reason)

    def close_root(self, db, root_id, reason):
        changed = db.execute(
            "UPDATE roots SET status='failed',error=? WHERE id=? AND status='open'",
            (reason, root_id),
        )
        if not changed.rowcount:
            return
        for task in db.execute(
            "SELECT * FROM tasks WHERE root_id=? AND status IN ('Open','Assigned')", (root_id,)
        ).fetchall():
            self.release_bids(db, task)
        db.execute(
            "UPDATE tasks SET status='Failed',lease_until=NULL,updated=? WHERE root_id=? AND status IN ('Open','Assigned')",
            (self.clock(), root_id),
        )
        self.event(db, "root_failed", "supervisor", root_id, reason=reason)

    def supervisor_lease(self, owner, *, seconds=30):
        with self.transaction() as db:
            old = db.execute("SELECT * FROM supervisor WHERE singleton=1").fetchone()
            if old and old["owner"] != owner and old["lease_until"] > self.clock():
                return False
            db.execute(
                "INSERT INTO supervisor VALUES(1,?,?) ON CONFLICT(singleton) DO UPDATE SET owner=excluded.owner,lease_until=excluded.lease_until",
                (owner, self.clock() + seconds),
            )
            return True

    def release_supervisor(self, owner):
        with self.transaction() as db:
            db.execute("DELETE FROM supervisor WHERE owner=?", (owner,))

    def history(self):
        with self.connection() as db:
            return [dict(row) for row in db.execute("SELECT * FROM events ORDER BY seq")]

    def verify_history(self):
        previous = "0" * 64
        for row in self.history():
            digest = hashlib.sha256(
                encoded(
                    [
                        row["created"],
                        row["actor"],
                        row["task_id"],
                        row["kind"],
                        row["data"],
                        previous,
                    ]
                ).encode()
            ).hexdigest()
            if row["previous_hash"] != previous or row["hash"] != digest:
                return False
            previous = digest
        return True

    def summary(self, root_id):
        with self.connection() as db:
            calls = [
                dict(row)
                for row in db.execute(
                    "SELECT * FROM calls WHERE root_id=? ORDER BY created", (root_id,)
                )
            ]
            payouts = db.execute(
                "SELECT COALESCE(SUM(w.delta),0) FROM wallets w JOIN tasks t ON t.id=w.task_id WHERE t.root_id=? AND w.kind='reward'",
                (root_id,),
            ).fetchone()[0]
        root = self.root(root_id)
        return {
            "root_id": root_id,
            "status": root["status"],
            "error": root["error"],
            "reward_cents": root["reward"],
            "paid_cents": payouts,
            "escrow_remaining_cents": root["reward"] - payouts,
            "tasks": self.tasks(root_id),
            "agents": self.agents(),
            "model_calls": calls,
            "input_tokens": sum(c["input_tokens"] for c in calls),
            "output_tokens": sum(c["output_tokens"] for c in calls),
            "calls_without_usage": sum(not c["usage_known"] for c in calls),
            "history_valid": self.verify_history(),
        }
