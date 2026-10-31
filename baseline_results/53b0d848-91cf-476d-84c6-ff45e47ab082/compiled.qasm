OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
u(pi/4,0,0) q[1];
cx q[0],q[1];
u(-pi/4,0,0) q[1];
cx q[0],q[1];
cx q[1],q[0];
