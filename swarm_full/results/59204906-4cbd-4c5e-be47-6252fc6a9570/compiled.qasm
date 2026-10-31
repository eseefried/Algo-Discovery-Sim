OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
u(0,0,0.7) q[0];
u(-1.0,0,0) q[0];
u(0,0,1.2) q[0];
u(1.0,0,0) q[0];
u(0,0,0.4) q[0];
