OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
u(pi/4,-pi/2,pi/2) q[1];
cx q[1],q[0];
u(0,0,-pi/2) q[1];
u(-pi/4,-pi/2,pi/2) q[1];
