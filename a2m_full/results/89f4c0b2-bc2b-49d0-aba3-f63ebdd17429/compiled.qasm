OPENQASM 2.0;
include "qelib1.inc";
qreg q[3];
u(0,0,pi) q[0];
u(0,0,pi) q[1];
u(pi/2,0,pi) q[2];
cx q[1],q[2];
u(pi/2,0,pi) q[2];
