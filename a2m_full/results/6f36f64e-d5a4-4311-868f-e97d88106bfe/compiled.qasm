OPENQASM 2.0;
include "qelib1.inc";
qreg q[1];
u(0.2,0,0) q[0];
u(0,0,-0.2) q[0];
u(-0.2,0,0) q[0];
u(0,0,0.2) q[0];
