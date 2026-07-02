import math

# Realistic study cards for all 10 subjects, structured by Subject -> Module
MOCK_CARDS = {
    "Engineering Mathematics III": {
        "Module 1: Laplace Transform": [
            {
                "title": "Laplace Transform Definition",
                "content": "The **Laplace Transform** converts a time-domain function $f(t)$ into a complex frequency-domain function $F(s)$.\n\nIt is defined mathematically by the integral:\n$$L\\{f(t)\\} = F(s) = \\int_{0}^{\\infty} e^{-st} f(t) dt$$\n\nwhere $s = \\sigma + j\\omega$ is a complex variable."
            },
            {
                "title": "Transforms of Standard Functions",
                "content": "Memorize these essential Laplace transforms for your exams:\n- $L\\{1\\} = \\frac{1}{s}$\n- $L\\{e^{at}\\} = \\frac{1}{s-a}$\n- $L\\{t^n\\} = \\frac{n!}{s^{n+1}}$\n- $L\\{\\sin(at)\\} = \\frac{a}{s^2 + a^2}$\n- $L\\{\\cos(at)\\} = \\frac{s}{s^2 + a^2}$"
            }
        ],
        "Module 2: Inverse Laplace Transform": [
            {
                "title": "Inverse Laplace Transform",
                "content": "The **Inverse Laplace Transform** converts $F(s)$ back into the time-domain $f(t)$:\n$$L^{-1}\\{F(s)\\} = f(t)$$\n\n*Common Technique*: Use **Partial Fraction Decomposition** to break complex fractions into standard terms, then apply standard inverse formulas (e.g. $L^{-1}\\{\\frac{1}{s-2}\\} = e^{2t}$)."
            },
            {
                "title": "Convolution Theorem",
                "content": "The Convolution Theorem simplifies finding the inverse Laplace transform of a product of two frequency-domain functions.\n\n**Theorem**:\n$$L^{-1}\\{F(s) \\cdot G(s)\\} = f(t) * g(t) = \\int_{0}^{t} f(u)g(t-u)du$$\n\nIt replaces complex frequency domain multiplications with time-domain integration."
            }
        ],
        "Module 3: Fourier Series": [
            {
                "title": "Fourier Series Introduction",
                "content": "A **Fourier Series** decomposes any periodic function $f(x)$ with period $2L$ into a sum of simple sines and cosines:\n$$f(x) = a_0 + \\sum_{n=1}^{\\infty} \\left( a_n \\cos\\left(\\frac{n\\pi x}{L}\\right) + b_n \\sin\\left(\\frac{n\\pi x}{L}\\right) \\right)$$\n\n*Application*: Analyzing periodic waveforms in power systems and music signals."
            },
            {
                "title": "Euler's Formulas",
                "content": "The coefficients $a_0, a_n, b_n$ of the Fourier Series are calculated using Euler's integrals:\n- $a_0 = \\frac{1}{2L} \\int_{-L}^{L} f(x) dx$\n- $a_n = \\frac{1}{L} \\int_{-L}^{L} f(x) \\cos\\left(\\frac{n\\pi x}{L}\\right) dx$\n- $b_n = \\frac{1}{L} \\int_{-L}^{L} f(x) \\sin\\left(\\frac{n\\pi x}{L}\\right) dx$"
            }
        ],
        "Module 4: Complex Variables": [
            {
                "title": "Cauchy-Riemann Equations",
                "content": "For a complex function $f(z) = u(x,y) + i v(x,y)$ to be analytic, it must satisfy the **Cauchy-Riemann (C-R) Equations**:\n$$\\frac{\\partial u}{\\partial x} = \\frac{\\partial v}{\\partial y} \\quad \\text{and} \\quad \\frac{\\partial u}{\\partial y} = -\\frac{\\partial v}{\\partial x}$$\n\nIf these partial derivatives are continuous, the function is differentiable."
            },
            {
                "title": "Conformal Mapping",
                "content": "A mapping $w = f(z)$ is **conformal** if it preserves the angle between curves in magnitude and direction.\n\n*Analytic Property*: Any transformation defined by an analytic function $f(z)$ is conformal at all points where the derivative $f'(z) \\neq 0$."
            }
        ],
        "Module 5: Linear Algebra & Matrices": [
            {
                "title": "Eigenvalues & Eigenvectors",
                "content": "For a square matrix $A$, a scalar $\\lambda$ and non-zero vector $v$ are **eigenvalue** and **eigenvector** if:\n$$A v = \\lambda v$$\n\nTo find $\\lambda$, solve the characteristic equation: $\\det(A - \\lambda I) = 0$."
            },
            {
                "title": "Cayley-Hamilton Theorem",
                "content": "The **Cayley-Hamilton Theorem** states that every square matrix satisfies its own characteristic equation.\n\nIf characteristic polynomial is $p(\\lambda) = \\lambda^2 - 5\\lambda + 6 = 0$, then matrix equation is:\n$$A^2 - 5A + 6I = 0$$\nThis theorem is useful for finding matrix inverses ($A^{-1}$) and higher powers ($A^n$)."
            }
        ],
        "Module 6: Vector Integration": [
            {
                "title": "Green's Theorem in Plane",
                "content": "Green's Theorem relates a line integral around a simple closed curve $C$ to a double integral over the region $D$ bounded by $C$:\n$$\\oint_C (P dx + Q dy) = \\iint_D \\left( \\frac{\\partial Q}{\\partial x} - \\frac{\\partial P}{\\partial y} \\right) dA$$\n\nIt simplifies circulation calculations in fluid flow mechanics."
            },
            {
                "title": "Stokes' Theorem",
                "content": "Stokes' Theorem extends Green's Theorem to 3D space, relating a surface integral of the curl of a vector field $F$ to a line integral of $F$ around the boundary curve $C$:\n$$\\oint_C F \\cdot dr = \\iint_S (\\nabla \\times F) \\cdot dS$$\n\nIt states that the circulation of a vector field is equal to its net curl over the surface."
            }
        ]
    },
    "Data Structures": {
        "Module 1: Introduction to Data Structures & Analysis": [
            {
                "title": "Data Structures Overview",
                "content": "A **Data Structure** is a systematic way of organizing and storing data in a computer so that it can be used efficiently.\n\n* **Linear**: Array, Linked List, Stack, Queue.\n* **Non-Linear**: Tree, Graph.\n\nChoosing the right structure depends on the operations needed (e.g. search, insert, delete) and their time complexity."
            },
            {
                "title": "Asymptotic Notation",
                "content": "To analyze algorithms, we use **Big-O Notation** which describes the upper bound of execution time as input size $N$ grows:\n- **Constant**: $O(1)$\n- **Logarithmic**: $O(\\log N)$\n- **Linear**: $O(N)$\n- **Log-linear**: $O(N \\log N)$\n- **Quadratic**: $O(N^2)$"
            }
        ],
        "Module 2: Linear Data Structures - Stacks and Queues": [
            {
                "title": "Stack Data Structure",
                "content": "A **Stack** is a linear data structure operating on **LIFO** (Last In, First Out) rules.\n\n* **Key Operations**:\n  - `push(x)`: Inserts element $x$ at top ($O(1)$).\n  - `pop()`: Removes top element ($O(1)$).\n  - `peek()`: Returns top element without removal ($O(1)$).\n* **Use Cases**: Undo/Redo buffers, function recursion call stacks, parenthesis matching."
            },
            {
                "title": "Queue Data Structure",
                "content": "A **Queue** is a linear data structure operating on **FIFO** (First In, First Out) rules.\n\n* **Key Operations**:\n  - `enqueue(x)`: Inserts element $x$ at the rear ($O(1)$).\n  - `dequeue()`: Removes element from the front ($O(1)$).\n* **Use Cases**: Printer task queues, CPU scheduling, bread-first search traversal."
            }
        ],
        "Module 3: Linked Lists": [
            {
                "title": "Linked Lists Overview",
                "content": "A **Linked List** is a linear data structure where elements are not stored in contiguous memory locations. Instead, each element is a separate object called a **Node**.\n\n* **Head**: The entry pointer to the first node.\n* **Tail**: The final node, whose pointer points to `NULL`.\n\nUnlike Arrays, you don't need to declare a fixed size in advance. Memory is allocated dynamically on-the-fly!"
            },
            {
                "title": "Search Operation Complexity",
                "content": "Searching for a value in a linked list requires a linear scan from `Head` to `Tail`:\n- **Best Case**: `O(1)` (value is at the Head).\n- **Worst Case**: `O(N)` (value is at the Tail or not present).\n\nEven if the list is **sorted**, you cannot perform Binary Search because you cannot access the middle element in `O(1)` time!"
            }
        ],
        "Module 4: Non-Linear Data Structures - Trees": [
            {
                "title": "Binary Search Tree",
                "content": "A **Binary Search Tree (BST)** is a binary tree where for each node:\n- All nodes in its **left** subtree have values less than the node's value.\n- All nodes in its **right** subtree have values greater than the node's value.\n\n*Search Time*: Average $O(\\log N)$, Worst case $O(N)$ (skewed tree)."
            },
            {
                "title": "AVL Trees (Balanced BST)",
                "content": "An **AVL Tree** is a self-balancing Binary Search Tree where the height difference (**Balance Factor**) between left and right subtrees of any node is at most 1:\n$$\\text{BF} = |\\text{height}(L) - \\text{height}(R)| \\le 1$$\n\nIf BF violates this, rotations (LL, RR, LR, RL) are performed. Balance ensures search is always $O(\\log N)$."
            }
        ],
        "Module 5: Non-Linear Data Structures - Graphs": [
            {
                "title": "Graph Representations",
                "content": "A **Graph** $G = (V, E)$ consists of vertices $V$ and edges $E$. Represented in memory via:\n1. **Adjacency Matrix**: A 2D array of size $|V| \\times |V|$ ($O(1)$ lookup, $O(V^2)$ space).\n2. **Adjacency List**: An array of lists of size $|V|$ (efficient space for sparse graphs, $O(V+E)$)."
            },
            {
                "title": "BFS vs DFS Traversal",
                "content": "* **Breadth-First Search (BFS)**: Explores vertices level-by-level using a **Queue** (good for finding shortest path in unweighted graphs).\n* **Depth-First Search (DFS)**: Explores deep along each branch before backtracking using a **Stack** or recursion.\n\n*Time Complexity* for both: $O(V + E)$."
            }
        ],
        "Module 6: Sorting and Searching Techniques": [
            {
                "title": "Quick Sort Partitioning",
                "content": "**Quick Sort** is a divide-and-conquer algorithm. It selects a 'pivot' element and partitions the array such that:\n- Elements smaller than pivot are on the left.\n- Elements larger than pivot are on the right.\n\n*Time Complexity*: Average $O(N \\log N)$, Worst case $O(N^2)$ (sorted input)."
            },
            {
                "title": "Binary Search Algorithm",
                "content": "**Binary Search** finds the position of a target value within a **sorted** array by repeatedly dividing the search interval in half.\n\n*Time Complexity*: $O(\\log N)$ since search space is halved at each step."
            }
        ]
    },
    "Signals and Systems": {
        "Module 1: Introduction to Signals and Systems": [
            {
                "title": "Continuous vs Discrete Signals",
                "content": "* **Continuous-Time (CT) Signals**: Defined for every value of time $t$ (e.g. analog audio voltage). Represented as $x(t)$.\n* **Discrete-Time (DT) Signals**: Defined only at discrete integer steps $n$ (e.g. digital audio samples). Represented as $x[n]$."
            },
            {
                "title": "Signal Classifications",
                "content": "Signals can be classified as:\n- **Periodic**: If $x(t) = x(t + T)$ for all $t$.\n- **Symmetric**: Even if $x(-t) = x(t)$, Odd if $x(-t) = -x(t)$.\n- **Energy vs. Power**: Energy signals have finite energy and zero average power; power signals have finite power and infinite energy."
            }
        ],
        "Module 2: Linear Time-Invariant (LTI) Systems": [
            {
                "title": "LTI Systems (Linear Time-Invariant)",
                "content": "A system is **LTI** if it satisfies two core mathematical properties:\n1. **Linearity**: Satisfies superposition ($H\\{a x_1 + b x_2\\} = a H\\{x_1\\} + b H\\{x_2\\}$).\n2. **Time-Invariance**: A time-shift in inputs causes an identical shift in outputs ($y(t-t_0) = H\\{x(t-t_0)\\}$).\n\nLTI systems are completely characterized by their **Impulse Response** $h(t)$."
            },
            {
                "title": "Convolution Integral",
                "content": "For a Continuous LTI system, the output $y(t)$ is the **convolution** of the input $x(t)$ and impulse response $h(t)$:\n$$y(t) = x(t) * h(t) = \\int_{-\\infty}^{\\infty} x(\\tau) h(t - \\tau) d\\tau$$"
            }
        ],
        "Module 3: Fourier Analysis of Continuous-Time Signals": [
            {
                "title": "Fourier Transform Definition",
                "content": "The **Continuous-Time Fourier Transform (CTFT)** maps a signal from time domain to frequency domain:\n$$X(j\\omega) = \\int_{-\\infty}^{\\infty} x(t) e^{-j\\omega t} dt$$\n\nIt decomposes a signal into its constituent complex exponential frequency components."
            },
            {
                "title": "Nyquist-Shannon Sampling Theorem",
                "content": "To perfectly reconstruct a continuous band-limited signal without distortion (**aliasing**), the sampling frequency $f_s$ must be at least twice the maximum frequency component $f_m$ of the signal:\n$$f_s \\ge 2 f_m$$\n\n$2 f_m$ is known as the **Nyquist Rate**."
            }
        ],
        "Module 4: Laplace Transform Analysis": [
            {
                "title": "Laplace ROC Properties",
                "content": "The **Region of Convergence (ROC)** is the range of $s$ values where the Laplace integral converges:\n- ROC of a right-sided signal is a right-half plane.\n- ROC cannot contain any poles.\n- For a system to be stable, the imaginary axis ($j\\omega$ axis) must lie inside the ROC."
            },
            {
                "title": "Transfer Function Stability",
                "content": "For a continuous system with transfer function $H(s) = \\frac{B(s)}{A(s)}$:\n- The roots of $A(s)$ are **poles**; roots of $B(s)$ are **zeros**.\n- The system is stable if and only if all poles have negative real parts (located in the left-half of the s-plane)."
            }
        ],
        "Module 5: Fourier Analysis of Discrete-Time Signals": [
            {
                "title": "DTFT Definition",
                "content": "The **Discrete-Time Fourier Transform (DTFT)** maps a discrete sequence $x[n]$ to a continuous periodic frequency spectrum:\n$$X(e^{j\\Omega}) = \\sum_{n=-\\infty}^{\\infty} x[n] e^{-j\\Omega n}$$\n\nUnlike CTFT, the DTFT spectrum is periodic with period $2\\pi$."
            },
            {
                "title": "Discrete Fourier Transform (DFT)",
                "content": "The **DFT** samples the continuous DTFT at $N$ discrete frequency points, making it suitable for digital processors:\n$$X[k] = \\sum_{n=0}^{N-1} x[n] e^{-j\\frac{2\\pi}{N} k n}$$\n*FFT* is just a fast $O(N \\log N)$ algorithm to compute the DFT."
            }
        ],
        "Module 6: Z-Transform Analysis": [
            {
                "title": "Z-Transform Definition",
                "content": "The **Z-Transform** is the discrete-time equivalent of the Laplace transform, mapping discrete sequences to the complex z-plane:\n$$X(z) = \\sum_{n=-\\infty}^{\\infty} x[n] z^{-n}$$\n\n*Region of Convergence (ROC)*: The set of values of $z$ for which the summation converges."
            },
            {
                "title": "Z-Plane Stability",
                "content": "A discrete-time LTI system is stable if and only if its Region of Convergence (ROC) contains the **unit circle** ($|z| = 1$). For causal systems, this means all system poles must lie *inside* the unit circle."
            }
        ]
    },
    "Engineering Mechanics": {
        "Module 1: System of Coplanar Forces": [
            {
                "title": "Coplanar Forces",
                "content": "Coplanar forces lie in a single plane. \n- **Resultant Force ($R$)**: The single force that produces the same effect as multiple forces:\n  $$R = \\sqrt{(\\sum F_x)^2 + (\\sum F_y)^2}$$\n- **Angle of Resultant ($\\theta$)**:\n  $$\\theta = \\tan^{-1}\\left(\\frac{|\\sum F_y|}{|\\sum F_x|}\\right)$$"
            },
            {
                "title": "Lami's Theorem",
                "content": "If three coplanar, concurrent forces act on a body keeping it in equilibrium, then each force is proportional to the sine of the angle between the other two forces.\n\n$$\\frac{P}{\\sin(\\alpha)} = \\frac{Q}{\\sin(\\beta)} = \\frac{R}{\\sin(\\gamma)}$$\n\n*Useful for*: Quick calculation of cable tensions or suspended reactions."
            }
        ],
        "Module 2: Equilibrium of Coplanar Force Systems": [
            {
                "title": "Conditions of Equilibrium",
                "content": "For a rigid body to remain in static equilibrium under coplanar forces:\n1. $\\sum F_x = 0$ (No horizontal translation)\n2. $\\sum F_y = 0$ (No vertical translation)\n3. $\\sum M_P = 0$ (No rotation about any arbitrary point $P$)"
            },
            {
                "title": "Types of Supports & Reactions",
                "content": "Supports exert reactions restricting motion:\n- **Roller Support**: 1 reaction perpendicular to surface.\n- **Hinge Support**: 2 reaction components (vertical & horizontal).\n- **Fixed Support**: 3 reactions (vertical, horizontal, and resisting moment)."
            }
        ],
        "Module 3: Friction and Truss Analysis": [
            {
                "title": "Friction & Laws of Friction",
                "content": "**Friction** is the resistive force acting tangent to the contact surface opposing relative motion.\n- **Limiting Friction ($F_m$)**: The maximum friction force when motion is impending:\n  $$F_m = \\mu_s N$$\n  where $\\mu_s$ is the coefficient of static friction and $N$ is the normal reaction force."
            },
            {
                "title": "Method of Joints (Trusses)",
                "content": "To solve a truss using the **Method of Joints**:\n1. Find external reactions using entire truss equilibrium.\n2. Select a joint with at most 2 unknown member forces.\n3. Apply $\\sum F_x = 0$ and $\\sum F_y = 0$ to solve forces."
            }
        ],
        "Module 4: Kinematics of Particles": [
            {
                "title": "Rectilinear Motion Equations",
                "content": "For constant acceleration $a$, kinematic equations are:\n1. $v = u + a t$\n2. $s = u t + \\frac{1}{2} a t^2$\n3. $v^2 = u^2 + 2 a s$\n\nwhere $u$ is initial velocity, $v$ is final velocity, and $s$ is displacement."
            },
            {
                "title": "Projectile Motion",
                "content": "A projectile exhibits horizontal motion at constant velocity ($a_x = 0$) and vertical motion under gravity ($a_y = -g$):\n- **Time of Flight**: $T = \\frac{2 u \\sin\\theta}{g}$\n- **Max Height**: $H = \\frac{u^2 \\sin^2\\theta}{2g}$\n- **Horizontal Range**: $R = \\frac{u^2 \\sin(2\\theta)}{g}$"
            }
        ],
        "Module 5: Kinematics of Rigid Bodies": [
            {
                "title": "Rotation about Fixed Axis",
                "content": "Angular motion equations mirror linear ones:\n1. $\\omega = \\omega_0 + \\alpha t$\n2. $\\theta = \\omega_0 t + \\frac{1}{2} \\alpha t^2$\n3. $\\omega^2 = \\omega_0^2 + 2 \\alpha \\theta$\n\nRelation to linear motion: $v = r\\omega$, $a_t = r\\alpha$, and $a_n = r\\omega^2$."
            },
            {
                "title": "Instantaneous Center of Rotation (ICR)",
                "content": "For a body undergoing General Plane Motion (translation + rotation), there exists a point in space (ICR) with zero velocity at that instant. The motion can be modeled as pure rotation about this ICR: $v = r \\omega$."
            }
        ],
        "Module 6: Kinetics of Particles": [
            {
                "title": "D'Alembert's Principle",
                "content": "D'Alembert's Principle translates a dynamic problem into an equivalent static equilibrium problem by introducing an **Inertia Force**:\n$$F_I = -m a$$\n\n**Equation of Motion**:\n$$\\sum F - m a = 0$$\n\nwhere $m$ is the mass and $a$ is the acceleration."
            },
            {
                "title": "Work-Energy Principle",
                "content": "The net work done by all forces acting on a particle equals the change in its kinetic energy:\n$$U_{1-2} = T_2 - T_1 = \\frac{1}{2} m v_2^2 - \\frac{1}{2} m v_1^2$$\n\nThis is ideal for systems involving force, displacement, and velocity without time."
            }
        ]
    },
    "Corporate Finance": {
        "Module 1: Introduction to Corporate Finance": [
            {
                "title": "Scope of Corporate Finance",
                "content": "Corporate Finance deals with three major strategic financial decisions:\n1. **Investment Decision**: Capital budgeting and resource allocation.\n2. **Financing Decision**: Debt-equity ratio and capital procurement.\n3. **Dividend Decision**: Reinvestment vs. shareholder payout strategies."
            },
            {
                "title": "Wealth Maximization Goal",
                "content": "While Profit Maximization focuses on short-term accounting net profit, **Wealth Maximization** aims to maximize the market value of the company's shares. It incorporates the time value of money, cash flows, and risk."
            }
        ],
        "Module 2: Time Value of Money": [
            {
                "title": "Compounding & Discounting",
                "content": "Money has time value because of inflation, opportunity cost, and risk:\n- **Future Value (FV)**: $FV = PV(1 + r)^n$\n- **Present Value (PV)**: $PV = \\frac{FV}{(1 + r)^n}$\n\nwhere $PV$ is present value, $r$ is interest rate, and $n$ is time periods."
            },
            {
                "title": "Annuities",
                "content": "An **Annuity** is a stream of equal periodic cash flows for a fixed duration:\n- **Present Value of Ordinary Annuity (PVA)**:\n  $$PVA = C \\cdot \\left[ \\frac{1 - (1+r)^{-n}}{r} \\right]$$\n  where $C$ is the periodic cash flow amount."
            }
        ],
        "Module 3: Capital Budgeting Decisions": [
            {
                "title": "Net Present Value (NPV)",
                "content": "NPV is the sum of present values of cash inflows minus cash outflows:\n$$NPV = \\sum_{t=1}^{n} \\frac{CF_t}{(1+r)^t} - CF_0$$\n\n*Decision Rule*: Accept the project if $NPV > 0$ since it adds value to the firm."
            },
            {
                "title": "Internal Rate of Return (IRR)",
                "content": "IRR is the discount rate that makes the Net Present Value of a project equal to zero:\n$$NPV = \\sum_{t=1}^{n} \\frac{CF_t}{(1+IRR)^t} - CF_0 = 0$$\n\n*Decision Rule*: Accept the project if $IRR > \\text{Cost of Capital}$."
            }
        ],
        "Module 4: Cost of Capital & WACC": [
            {
                "title": "Cost of Debt & Equity",
                "content": "- **Cost of Debt ($K_d$)**: $K_d = r(1 - T)$, where $T$ is tax rate (debt interest is tax-deductible).\n- **Cost of Equity ($K_e$)**: Using CAPM model:\n  $$K_e = R_f + \\beta(R_m - R_f)$$\n  where $R_f$ is risk-free rate, $\\beta$ is systematic risk, and $R_m$ is market return."
            },
            {
                "title": "WACC Formula",
                "content": "Weighted Average Cost of Capital (WACC) is the average cost of all financing sources weighted by their proportions in the capital structure:\n$$WACC = W_e K_e + W_d K_d$$\n\nwhere $W_e, W_d$ are equity and debt weights."
            }
        ],
        "Module 5: Working Capital Management": [
            {
                "title": "Operating Cycle",
                "content": "The **Operating Cycle** is the duration between raw material purchase and cash receipt from sales:\n$$\\text{Operating Cycle} = \\text{ICP} + \\text{RCP} - \\text{PCP}$$\n\nwhere $ICP$ is inventory conversion period, $RCP$ is receivables collection period, and $PCP$ is payables deferral period."
            },
            {
                "title": "Cash Management Models",
                "content": "- **Baumol Model**: Balances cash transaction costs against interest forgone (similar to EOQ).\n- **Miller-Orr Model**: Sets lower and upper cash limits based on daily variance in cash flows."
            }
        ],
        "Module 6: Dividend Policy and Decisions": [
            {
                "title": "Walter's Model",
                "content": "Walter's Model states that dividend policy depends on the relationship between return on investment ($r$) and cost of capital ($k$):\n$$P = \\frac{D + \\frac{r}{k}(E - D)}{k}$$\n\nwhere $P$ is market price, $D$ is dividend, and $E$ is earnings per share."
            },
            {
                "title": "MM Dividend Hypothesis",
                "content": "Modigliani and Miller (MM) argue that dividend policy is **irrelevant** to share price in a perfect capital market. Share value is determined solely by the firm's earnings power and investment policy, not payout distribution."
            }
        ]
    },
    "Financial Accounting": {
        "Module 1: Accounting Principles and Bookkeeping": [
            {
                "title": "Accounting Concepts",
                "content": "- **Going Concern Concept**: Assume business operates indefinitely.\n- **Business Entity Concept**: Business is separate from its owner.\n- **Dual Aspect Concept**: Every transaction has equal debit and credit aspects: \n  $$\\text{Assets} = \\text{Liabilities} + \\text{Capital}$$\n  This is the fundamental accounting equation."
            },
            {
                "title": "Journal and Ledger",
                "content": "- **Journal**: The book of original entry where transactions are recorded chronologically.\n- **Ledger**: The principal book of accounts where journal entries are classified and posted to individual accounts."
            }
        ],
        "Module 2: Preparation of Financial Statements": [
            {
                "title": "Trading & Profit & Loss",
                "content": "- **Trading A/c**: Determines **Gross Profit** (Sales - Cost of Goods Sold).\n- **Profit & Loss A/c**: Determines **Net Profit** by subtracting indirect expenses (rent, salaries, admin) from gross profit."
            },
            {
                "title": "Balance Sheet Structure",
                "content": "The **Balance Sheet** is a statement of financial position at a specific date:\n- **Assets**: Current Assets (Cash, inventory) + Fixed Assets (Machinery, buildings).\n- **Liabilities**: Current Liabilities (Creditors) + Long-term Debt + Capital (Equity)."
            }
        ],
        "Module 3: Depreciation and Inventory Valuation": [
            {
                "title": "Depreciation Methods",
                "content": "- **Straight Line Method (SLM)**: Constant depreciation charge each year:\n  $$\\text{Depreciation} = \\frac{\\text{Cost} - \\text{Scrap Value}}{\\text{Useful Life}}$$\n- **Written Down Value (WDV)**: Depreciation is a fixed percentage of the reducing book value."
            },
            {
                "title": "Inventory Valuation Rules",
                "content": "- **FIFO**: Assumes oldest stock is sold first.\n- **LIFO**: Assumes newest stock is sold first.\n- **Weighted Average**: Average cost is computed after each purchase.\n\n*Accounting Rule*: Inventory is valued at **Cost or Net Realizable Value (NRV), whichever is lower**."
            }
        ],
        "Module 4: Partnership Accounts": [
            {
                "title": "Partnership Goodwill",
                "content": "Goodwill is an intangible asset representing business reputation. Methods of valuation:\n1. **Average Profit Method**: Average profit multiplied by number of years' purchase.\n2. **Super Profit Method**: profits above normal industry return multiplied by years' purchase."
            },
            {
                "title": "Reconstitution of Firm",
                "content": "On admission/retirement of a partner:\n- Prepare **Revaluation Account** to adjust asset/liability values.\n- Distribute revaluation profit/losses to old partners in their old profit-sharing ratio."
            }
        ],
        "Module 5: Company Accounts": [
            {
                "title": "Share Capital Types",
                "content": "- **Authorized Capital**: Maximum shares a company can issue.\n- **Issued Capital**: Capital offered to the public.\n- **Subscribed Capital**: Capital taken up by the public.\n- **Paid-up Capital**: Amount paid by shareholders."
            },
            {
                "title": "Forfeiture of Shares",
                "content": "If a shareholder fails to pay allotment or call money, the company can forfeit their shares. Capital is debited, Unpaid Calls are credited, and the amount paid so far is transferred to the **Share Forfeiture Account**."
            }
        ],
        "Module 6: Financial Statement Ratio Analysis": [
            {
                "title": "Liquidity Ratios",
                "content": "- **Current Ratio**: Current Assets / Current Liabilities (Ideal = 2:1).\n- **Quick Ratio**: (Current Assets - Inventory - Prepaid Expenses) / Current Liabilities (Ideal = 1:1)."
            },
            {
                "title": "Profitability Ratios",
                "content": "- **Gross Profit Ratio**: $\\frac{\\text{Gross Profit}}{\\text{Net Sales}} \\times 100$\n- **Net Profit Ratio**: $\\frac{\\text{Net Profit}}{\\text{Net Sales}} \\times 100$\n- **Return on Equity (ROE)**: $\\frac{\\text{Net Income}}{\\text{Shareholder's Equity}} \\times 100$"
            }
        ]
    },
    "Marketing Management": {
        "Module 1: Introduction to Marketing & 4Ps": [
            {
                "title": "Marketing vs. Selling",
                "content": "- **Selling Concept**: Focuses on seller needs, promoting existing products via aggressive sales methods.\n- **Marketing Concept**: Focuses on customer needs, creating value and building long-term customer relationships."
            },
            {
                "title": "The 4 Ps of Marketing",
                "content": "1. **Product**: Features, design, branding, packaging.\n2. **Price**: List price, discounts, payment period.\n3. **Place**: Distribution channels, logistics, locations.\n4. **Promotion**: Advertising, public relations, sales promotion."
            }
        ],
        "Module 2: Consumer Buying Behavior": [
            {
                "title": "Consumer Buying Process",
                "content": "Consumers progress through 5 key stages when purchasing:\n1. Problem/Need Recognition\n2. Information Search\n3. Evaluation of Alternatives\n4. Purchase Decision\n5. Post-Purchase Behavior (Cognitive Dissonance checks)"
            },
            {
                "title": "Influences on Behavior",
                "content": "- **Cultural**: Subculture, social class.\n- **Social**: Reference groups, family, roles.\n- **Personal**: Age, occupation, lifestyle.\n- **Psychological**: Motivation, perception, learning, beliefs."
            }
        ],
        "Module 3: Market Segmentation, Targeting & Positioning (STP)": [
            {
                "title": "Market Segmentation Bases",
                "content": "Segmenting a market means dividing it into distinct consumer groups:\n- **Geographic**: Region, city size, climate.\n- **Demographic**: Age, gender, income, education.\n- **Psychographic**: Social class, lifestyle, personality.\n- **Behavioral**: Occasions, user status, loyalty."
            },
            {
                "title": "Product Positioning",
                "content": "Positioning is the act of designing the company's offering to occupy a distinctive place in the mind of the target market (e.g. Volvo positioning as 'Safety', Apple as 'Innovation')."
            }
        ],
        "Module 4: Product Life Cycle and Pricing Strategies": [
            {
                "title": "Product Life Cycle (PLC)",
                "content": "A product goes through 4 distinct stages:\n1. **Introduction**: High costs, low sales, negative profit.\n2. **Growth**: Rapid sales growth, rising profit.\n3. **Maturity**: Peak sales, intense competition, plateauing profit.\n4. **Decline**: Falling sales, product pruning, cost minimization."
            },
            {
                "title": "New Product Pricing",
                "content": "- **Market Skimming**: Set high initial prices to 'skim' revenues from premium buyers.\n- **Market Penetration**: Set a low initial price to attract a large volume of buyers and market share."
            }
        ],
        "Module 5: Distribution Channels and Promotion": [
            {
                "title": "Channel Intensity",
                "content": "- **Intensive Distribution**: Stocking products in as many outlets as possible (e.g. soft drinks).\n- **Selective Distribution**: Use of more than one, but fewer than all outlets (e.g. appliances).\n- **Exclusive Distribution**: Giving limited dealers exclusive rights to distribute (e.g. luxury cars)."
            },
            {
                "title": "Promotion Mix Elements",
                "content": "Companies communicate value via:\n- **Advertising**: Paid non-personal presentation.\n- **Personal Selling**: Face-to-face interaction.\n- **Sales Promotion**: Short-term incentives (coupons, discounts).\n- **Public Relations**: Building good corporate image."
            }
        ],
        "Module 6: Digital & Social Media Marketing": [
            {
                "title": "SEO vs SEM",
                "content": "- **Search Engine Optimization (SEO)**: Optimizing website content to rank organically in search engine result pages.\n- **Search Engine Marketing (SEM)**: Paid search advertising (e.g. Google Ads) bidding on keywords to drive traffic."
            },
            {
                "title": "Social Media Engagement",
                "content": "Brands leverage social platforms (Instagram, LinkedIn, YouTube) to create interactive content, run influencer campaigns, and gather customer feedback to build community trust."
            }
        ]
    },
    "Human Resource Management": {
        "Module 1: Introduction to HRM": [
            {
                "title": "Core Functions of HRM",
                "content": "- **Managerial**: Planning, organizing, directing, controlling.\n- **Operative**: Procurement (recruitment), Development (training), Compensation, Integration, and Maintenance of workforce."
            },
            {
                "title": "Strategic HRM",
                "content": "Strategic HRM links human resource policies directly to organizational strategic objectives (e.g. aligning hiring profiles with long-term digital transformation plans)."
            }
        ],
        "Module 2: HR Planning and Job Analysis": [
            {
                "title": "HRP Process",
                "content": "Human Resource Planning involves:\n1. Analyzing organizational plans.\n2. Forecasting HR demand (needs).\n3. Forecasting HR supply (internal/external talent pool).\n4. Formulating plans to resolve deficits or surpluses."
            },
            {
                "title": "Job Analysis Outcomes",
                "content": "Job Analysis produces two essential documents:\n- **Job Description (JD)**: Summary of tasks, duties, and responsibilities.\n- **Job Specification (JS)**: Minimum human qualities, education, and skills required."
            }
        ],
        "Module 3: Recruitment, Selection & Induction": [
            {
                "title": "Recruitment Sources",
                "content": "- **Internal**: Promotions, transfers, employee referrals (cost-effective, boosts morale).\n- **External**: Campus placements, job portals, advertisements, agencies (brings fresh talent)."
            },
            {
                "title": "Selection Steps",
                "content": "Selection is a negative process of weeding out unsuitable candidates:\n`Application Screening ➔ Selection Tests ➔ Interview ➔ Reference Checks ➔ Medical Exam ➔ Job Offer`"
            }
        ],
        "Module 4: Training & Management Development": [
            {
                "title": "Training Methods",
                "content": "- **On-the-Job**: Apprenticeship, job instruction training (learning while working).\n- **Off-the-Job**: Lectures, case studies, vestibule training, role-playing (focuses on learning away from workspace stress)."
            },
            {
                "title": "Evaluating Training",
                "content": "Using **Kirkpatrick's Model**:\n1. **Reaction**: Did employees like the training?\n2. **Learning**: Did they acquire knowledge?\n3. **Behavior**: Did their job habits change?\n4. **Results**: Did business metrics (e.g. sales, productivity) improve?"
            }
        ],
        "Module 5: Performance Appraisal & Compensation Planning": [
            {
                "title": "Performance Appraisal Methods",
                "content": "- **Traditional**: Graphic rating scales, confidential reports.\n- **Modern**: Management by Objectives (MBO), 360-degree feedback (gathering ratings from peers, subordinates, managers, and clients)."
            },
            {
                "title": "Job Evaluation",
                "content": "Job Evaluation determines the relative worth of different jobs in an organization to establish fair, equitable salary structures (using ranking or point systems)."
            }
        ],
        "Module 6: Industrial Relations & Employee Welfare": [
            {
                "title": "Industrial Disputes Resolution",
                "content": "Machinery for settling disputes in India:\n- **Conciliation**: Third party facilitates discussion.\n- **Arbitration**: Mutual agreement to accept third party decision.\n- **Adjudication**: Compulsory legal settlement by labor court/tribunal."
            },
            {
                "title": "Collective Bargaining",
                "content": "Collective Bargaining is the process of negotiation between employee representatives (trade unions) and management to reach a mutual agreement on wages, hours, and working conditions."
            }
        ]
    },
    "Macroeconomics": {
        "Module 1: National Income Accounting": [
            {
                "title": "GDP vs GNP",
                "content": "- **Gross Domestic Product (GDP)**: Market value of all final goods/services produced *within the country's borders* in a year.\n- **Gross National Product (GNP)**: GDP + Net Factor Income from Abroad (NFIA) (production by citizens globally)."
            },
            {
                "title": "Circular Flow of Income",
                "content": "In a 2-sector economy (Household & Firms):\n- Households supply factors (labor, capital) and receive income.\n- Firms supply goods/services and receive consumption expenditure.\nIncome circular flow ensures: $\\text{Total Income} = \\text{Total Output} = \\text{Total Expenditure}$."
            }
        ],
        "Module 2: Keynesian Demand Side Economics": [
            {
                "title": "Keynesian Consumption Function",
                "content": "Keynes asserted that consumption depends on disposable income $Y_d$:\n$$C = a + b Y_d$$\n\nwhere $a$ is autonomous consumption (spending when income is zero), and $b$ is Marginal Propensity to Consume ($MPC = \\frac{\\Delta C}{\\Delta Y}$)."
            },
            {
                "title": "Investment Multiplier",
                "content": "The multiplier ($k$) shows how an initial change in investment $\\Delta I$ leads to a larger change in national income $\\Delta Y$:\n$$k = \\frac{\\Delta Y}{\\Delta I} = \\frac{1}{1 - MPC} = \\frac{1}{MPS}$$\n\nIf $MPC = 0.8$, then multiplier $k = \\frac{1}{1 - 0.8} = 5$."
            }
        ],
        "Module 3: Money Supply, Banking & Monetary Policy": [
            {
                "title": "Central Bank Instruments",
                "content": "The central bank (RBI) controls money supply using:\n- **Quantitative**: repo rate, reverse repo rate, Cash Reserve Ratio (CRR), Statutory Liquidity Ratio (SLR).\n- **Qualitative**: margin requirements, moral suasion, credit rationing."
            },
            {
                "title": "Inflation & Unemployment (Phillips Curve)",
                "content": "The **Phillips Curve** shows an inverse relationship between inflation and unemployment in the short run. Lowering unemployment often causes temporary wage inflation."
            }
        ],
        "Module 4: Public Finance and Fiscal Policy": [
            {
                "title": "Fiscal Policy Objectives",
                "content": "Fiscal Policy involves the use of government taxation and expenditure to manage aggregate demand. During recessions, expansionary policy (increasing spending, cutting taxes) is used to boost employment."
            },
            {
                "title": "Deficit Indicators",
                "content": "- **Fiscal Deficit**: Total Expenditure - Total Receipts (excluding borrowings).\n- **Revenue Deficit**: Revenue Expenditure - Revenue Receipts.\n- **Primary Deficit**: Fiscal Deficit - Interest Payments."
            }
        ],
        "Module 5: Business Cycles and Economic Growth": [
            {
                "title": "Business Cycle Phases",
                "content": "Business cycles are fluctuations in aggregate economic activity:\n`Expansion (Growth) ➔ Peak ➔ Contraction (Recession) ➔ Trough (Lowest Point)`\nStabilization policies aim to smoothen these peaks and troughs."
            },
            {
                "title": "Harrod-Domar Growth Model",
                "content": "The model states that economic growth rate ($g$) depends on the savings rate ($s$) and the incremental capital-output ratio ($v$):\n$$g = \\frac{s}{v}$$\n\nTo increase growth, a country must either save more or improve capital efficiency (lower $v$)."
            }
        ],
        "Module 6: International Trade and Balance of Payments": [
            {
                "title": "Comparative Advantage",
                "content": "David Ricardo's theory states that a country should specialize in producing and exporting goods that it can produce at a lower **opportunity cost** compared to other nations, even if it has an absolute advantage in all goods."
            },
            {
                "title": "Balance of Payments (BOP)",
                "content": "BOP is a double-entry record of all economic transactions between a country and the rest of the world:\n- **Current Account**: Trade in goods/services, unilateral transfers.\n- **Capital Account**: FDI, external borrowings, portfolio investments."
            }
        ]
    },
    "Business Law": {
        "Module 1: Indian Contract Act 1872": [
            {
                "title": "Essentials of Valid Contract",
                "content": "According to Section 10, a valid contract requires:\n1. Offer and acceptance.\n2. Lawful consideration.\n3. Capacity of parties (major, sound mind).\n4. Free consent (no coercion, fraud, mistake).\n5. Lawful object."
            },
            {
                "title": "Breach of Contract Remedies",
                "content": "When a party breaches a contract, the injured party can:\n- Rescind the contract.\n- Sue for damages (liquidated/unliquidated).\n- Sue for specific performance.\n- Sue for injunction (preventing an action)."
            }
        ],
        "Module 2: Indemnity, Guarantee, Pledge & Agency": [
            {
                "title": "Indemnity vs Guarantee",
                "content": "- **Indemnity**: Contract to save a party from loss caused by promisor or third party (2 parties).\n- **Guarantee**: Contract to perform promise or discharge liability of a third party in case of default (3 parties: principal debtor, creditor, surety)."
            },
            {
                "title": "Pledge Definition",
                "content": "A **Pledge** is a special type of bailment where goods are deposited as security for payment of a debt or performance of a promise. The bailor is the *Pledger* (Pawnor) and the bailee is the *Pledgee* (Pawnee)."
            }
        ],
        "Module 3: Sale of Goods Act 1930": [
            {
                "title": "Conditions vs Warranties",
                "content": "- **Condition**: An essential stipulation to the main purpose of the contract. Breach gives right to reject contract and claim damages.\n- **Warranty**: A collateral stipulation. Breach only gives right to claim damages, not reject goods."
            },
            {
                "title": "Unpaid Seller Rights",
                "content": "An unpaid seller has rights against the goods:\n1. **Right of Lien**: Retaining goods until payment.\n2. **Right of Stoppage in Transit**: Stopping goods in transport if buyer is insolvent.\n3. **Right of Resale**: Reselling goods under specific conditions."
            }
        ],
        "Module 4: Negotiable Instruments Act 1881": [
            {
                "title": "Negotiable Instruments",
                "content": "Negotiable instruments are transferable documents representing money:\n- **Promissory Note**: Unconditional undertaking to pay (2 parties).\n- **Bill of Exchange**: Unconditional order to pay (3 parties: drawer, drawee, payee).\n- **Cheque**: Bill of exchange drawn on a specified banker."
            },
            {
                "title": "Section 138 (Cheque Dishonor)",
                "content": "Dishonor of a cheque due to insufficiency of funds is a **criminal offense** punishable by imprisonment up to 2 years, or a fine up to twice the cheque amount, or both. A legal notice must be served to the drawer within 30 days."
            }
        ],
        "Module 5: Companies Act 2013": [
            {
                "title": "MoA and AoA",
                "content": "- **Memorandum of Association (MoA)**: The charter of the company defining its constitution, name, registered office, and objects (external relations).\n- **Articles of Association (AoA)**: The bylaws governing internal management, shares, and board powers."
            },
            {
                "title": "Separate Legal Entity",
                "content": "A company is a separate legal person distinct from its members (Salomon v. Salomon case). It can own property, sue, and be sued in its own name, and features perpetual succession and limited liability."
            }
        ],
        "Module 6: Consumer Protection Act 2019": [
            {
                "title": "Consumer Redressal Forums",
                "content": "Three-tier quasi-judicial machinery for consumer disputes:\n1. **District Commission**: Claims up to ₹1 crore.\n2. **State Commission**: Claims between ₹1 crore and ₹10 crore.\n3. **National Commission**: Claims exceeding ₹10 crore."
            },
            {
                "title": "Product Liability",
                "content": "Under the 2019 Act, a product manufacturer, seller, or service provider is liable to compensate for any harm caused by a defective product or deficient service, removing the old 'caveat emptor' (buyer beware) shield."
            }
        ]
    }
}

SUBJECT_ALIASES = {
    "engineering mathematics iii": "Engineering Mathematics III",
    "engineering maths 3": "Engineering Mathematics III",
    "maths": "Engineering Mathematics III",
    "data structures": "Data Structures",
    "signals and systems": "Signals and Systems",
    "signals & systems": "Signals and Systems",
    "engineering mechanics": "Engineering Mechanics",
    "mechanics": "Engineering Mechanics",
    "corporate finance": "Corporate Finance",
    "finance": "Corporate Finance",
    "financial accounting": "Financial Accounting",
    "accounting": "Financial Accounting",
    "marketing management": "Marketing Management",
    "marketing": "Marketing Management",
    "human resource management": "Human Resource Management",
    "human resource": "Human Resource Management",
    "hrm": "Human Resource Management",
    "macroeconomics": "Macroeconomics",
    "economics": "Macroeconomics",
    "business law": "Business Law",
    "law": "Business Law"
}

def get_mock_study_plan(subject: str, duration: int, module_filter: str = "any module") -> str:
    """
    Generates a realistic, highly technical sequence of study cards
    for a given subject matching the duration, optionally filtering by module.
    """
    num_cards = max(3, min(8, round(duration / 2.5)))
    
    # 1. Normalize subject key matching using aliases
    subject_key = subject.lower().strip()
    matched_subject = SUBJECT_ALIASES.get(subject_key)
    
    # 2. Try matching by word subsets to avoid loose false positives
    if not matched_subject:
        subject_words = set(subject_key.split())
        for alias, canonical_name in SUBJECT_ALIASES.items():
            alias_words = set(alias.split())
            if subject_words.issubset(alias_words) or alias_words.issubset(subject_words):
                matched_subject = canonical_name
                break
                
    if not matched_subject:
        # Default fallback is Data Structures
        matched_subject = "Data Structures"
        
    subject_data = MOCK_CARDS[matched_subject]
    
    # 2. Filter by module if specified
    cards_source = []
    normalized_filter = module_filter.lower().strip() if module_filter else "any module"
    
    if normalized_filter != "any module" and normalized_filter != "":
        # Find matching module key
        matched_module = None
        for mod_name in subject_data.keys():
            if normalized_filter in mod_name.lower():
                matched_module = mod_name
                break
        
        if matched_module:
            cards_source = subject_data[matched_module]
            
    if not cards_source:
        # If no module matched or "any module" was selected, flatten all modules
        for mod_cards in subject_data.values():
            cards_source.extend(mod_cards)
            
    # 3. Construct cards list up to num_cards length
    selected_cards = []
    for i in range(num_cards):
        card_data = cards_source[i % len(cards_source)]
        card_num = i + 1
        
        # Add warning banner on the first card
        banner = ""
        if i == 0:
            banner = "> ⚠️ **Demo Mode Active**: Gemini API quota limit reached. Serving pre-compiled syllabus flashcards for testing.\n\n"
            
        card_md = f"# Card {card_num}: {card_data['title']}\n{banner}{card_data['content']}"
        selected_cards.append(card_md)
        
    return "\n\n---\n\n".join(selected_cards)
