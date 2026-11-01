OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
u(0,0,0.5) q[0];
u(pi/2,0,pi) q[0];
u(1.0,-pi/2,pi/2) q[1];
cx q[1],q[0];
u(pi/2,0,pi) q[0];
