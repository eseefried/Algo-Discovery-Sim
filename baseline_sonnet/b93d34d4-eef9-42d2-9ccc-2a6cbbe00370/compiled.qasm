OPENQASM 2.0;
include "qelib1.inc";
qreg q[2];
u(-pi/2,-pi/2,pi/2) q[0];
u(0,0,1.0) q[0];
