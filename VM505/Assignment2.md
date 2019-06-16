# Assignment 2

## Modify the demo code to solve the diff eqn

$$
-u_{,xx}+u+x^3=0,\ \ x\in(0,1)
$$

### (1) $u(0) = u(1) = 0$

```matlab
% Assignment 2
% pre-processing
nel = 12; nnode = nel + 1; a = 0; b = 1;
x_nodes = linspace(a, b, nnode);

% assembly
% K = spalloc(nnode, nnode, 3*nnode); 
K = zeros(nnode);
% equivalent to zeros(nnode)
F = zeros(nnode, 1);
for e = 1:nel
    % coordinates of nodes of element e
    xe = x_nodes([e, e+1]);
    [ke, fe] = elementcode1(xe);
    K([e, e+1], [e, e+1]) = K([e, e+1], [e, e+1]) + ke;
    F([e, e+1]) = F([e, e+1]) + fe;
end

% solve
K_active = K(2:end-1, 2:end-1);
F_active = F(2:end-1, 1);

d_active = K_active\F_active;
d = [0; d_active; 0];
% post-processing
plot(x_nodes,d,'r');
hold on;
scatter(x_nodes,-x_nodes.^3-6.*x_nodes+7*sinh(x_nodes)/sinh(1),'k');


function [ke,fe] = elementcode1(xe)
nquad = 2;
weights = [1.0, 1.0];
xis = [-1/sqrt(3), 1/sqrt(3)];
ke = zeros(length(xe));
fe = zeros(length(xe),1);

for iquad = 1 : nquad
    xi = xis(iquad);
    Ns = [(1-xi)/2, (1+xi)/2]'; %shape functions
    dNdxis = [-1/2, 1/2]'; %shape function derivatives
    x = xe * Ns;
    j = xe * dNdxis; % jacobian
    A = 1;
    dNdxs = dNdxis / j;
    ke = ke + Ns * Ns' * weights(iquad) * j ...
        + A * dNdxs * dNdxs' * weights(iquad) * j;
    
    p = -x^3;
    fe = fe + p * Ns * weights(iquad) * j;
end
end
```

![](C:\Users\xzhang\Documents\JI\VM505FiniteElementMethods\Assignments\asgnmt2_1.jpg)

### (2) $u'(0) = u(1) = 0$

```matlab
% Assignment 2
% pre-processing
nel = 12; nnode = nel + 1; a = 0; b = 1;
x_nodes = linspace(a, b, nnode);

% assembly
% K = spalloc(nnode, nnode, 3*nnode); 
K = zeros(nnode);
% equivalent to zeros(nnode)
F = zeros(nnode, 1);
for e = 1:nel
    % coordinates of nodes of element e
    xe = x_nodes([e, e+1]);
    [ke, fe] = elementcode2(xe);
    K([e, e+1], [e, e+1]) = K([e, e+1], [e, e+1]) + ke;
    F([e, e+1]) = F([e, e+1]) + fe;
end


% solve
K_active = K(1:end-1, 1:end-1);
F_active = F(1:end-1, 1);

d_active = K_active\F_active;
d = [d_active; 0];
% post-processing
plot(x_nodes,d,'r');
hold on;
scatter(x_nodes,-x_nodes.^3 - 6*x_nodes ...
    + (7.0-6.0*sinh(1.0))*cosh(x_nodes) / cosh(1.0) + 6.0*sinh(x_nodes),'k');
xlabel('x')
ylabel('u')
legend('FEM','Exact Solution')

function [ke,fe] = elementcode2(xe)
nquad = 2;
weights = [1.0, 1.0];
xis = [-1/sqrt(3), 1/sqrt(3)];
ke = zeros(length(xe));
fe = zeros(length(xe),1);

for iquad = 1 : nquad
    xi = xis(iquad);
    Ns = [(1-xi)/2, (1+xi)/2]'; %shape functions
    dNdxis = [-1/2, 1/2]'; %shape function derivatives
    x = xe * Ns;
    j = xe * dNdxis; % jacobian
    A = 1;
    dNdxs = dNdxis / j;
    ke = ke + Ns * Ns' * weights(iquad) * j ...
        + A * dNdxs * dNdxs' * weights(iquad) * j;
    
    p = -x^3;
    fe = fe + p * Ns * weights(iquad) * j;
end
end
```

![Alt text](C:\Users\xzhang\Documents\JI\VM505FiniteElementMethods\Assignments\asgnmt2_2.jpg)

### (3) $u'(0) - u(0) = u(1) = 0$

```matlab
% Assignment 2
% pre-processing
nel = 12; nnode = nel + 1; a = 0; b = 1;
x_nodes = linspace(a, b, nnode);

% assembly
% K = spalloc(nnode, nnode, 3*nnode); 
K = zeros(nnode);
% equivalent to zeros(nnode)
F = zeros(nnode, 1);
for e = 1:nel
    % coordinates of nodes of element e
    xe = x_nodes([e, e+1]);
    [ke, fe] = elementcode3(xe);
    K([e, e+1], [e, e+1]) = K([e, e+1], [e, e+1]) + ke;
    F([e, e+1]) = F([e, e+1]) + fe;
end

K(1, 1) = K(1, 1) + 1;

% solve
K_active = K(1:end-1, 1:end-1);
F_active = F(1:end-1, 1);

d_active = K_active\F_active;
d = [d_active; 0];
% post-processing
plot(x_nodes,d,'r');
hold on;
scatter(x_nodes,-x_nodes.^3 - 6*x_nodes ...
    +7.0*exp(x_nodes-1) + 3*exp(x_nodes-2) - 3*exp(-x_nodes) ,'k');
xlabel('x')
ylabel('u')
legend('FEM','Exact Solution')

function [ke,fe] = elementcode3(xe)
nquad = 2;
weights = [1.0, 1.0];
xis = [-1/sqrt(3), 1/sqrt(3)];
ke = zeros(length(xe));
fe = zeros(length(xe),1);

for iquad = 1 : nquad
    xi = xis(iquad);
    Ns = [(1-xi)/2, (1+xi)/2]'; %shape functions
    dNdxis = [-1/2, 1/2]'; %shape function derivatives
    x = xe * Ns;
    j = xe * dNdxis; % jacobian
    A = 1;
    dNdxs = dNdxis / j;
    ke = ke + Ns * Ns' * weights(iquad) * j ...
        + A * dNdxs * dNdxs' * weights(iquad) * j;
    
    p = -x^3;
    fe = fe + p * Ns * weights(iquad) * j;
end
end
```

![Alt text](C:\Users\xzhang\Documents\JI\VM505FiniteElementMethods\Assignments\asgnmt2_3.jpg)