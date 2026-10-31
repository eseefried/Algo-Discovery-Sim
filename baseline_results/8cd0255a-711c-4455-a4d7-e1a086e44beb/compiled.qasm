OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
u(pi,pi/2,pi/2) q[0];
u(pi,0,pi) q[0];
u(0,0,pi) q[0];
