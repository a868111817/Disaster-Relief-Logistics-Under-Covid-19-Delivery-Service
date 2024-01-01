# Disaster-Relief-Logistics-Under-Covid-19-Delivery-Service

## Background: Disaster Relief Logistics

Our project is inspired by the research paper titled "A multi-objective robust stochastic programming model for disaster relief logistics under uncertainty" by Ali Bozorgi-Amiri et al, published in the OR Spectrum journal in 2011. Their model is a multi-objective approach with the following objectives:

1. Minimize the total cost and its variance.
2. Maximize the satisfaction level of the least satisfied affected area.

To address the uncertainty inherent in disaster scale, their model utilizes discrete scenario analysis to incorporate stochastic factors.

## Motivation

With the gradual normalization of Covid-19 threats, it becomes imperative to devise strategies for responding to disasters during the pandemic. Let's consider an hypothetical scenario where an earthquake has damaged a hospital that was treating numerous Covid-19 confirmed cases. Now, resources must be delivered to this hospital without any further human contact. In this scenario, we propose the use of contactless stations (CSs) instead of the RDCs (Regional Distribution Centers) suggested by Bozorgi-Amiri.

CSs would facilitate the delivery of resources through self-driving cars, eliminating the risks associated with frequent human interactions. Furthermore, CSs would reduce transportation costs as there would be no need for human drivers. We envision that CSs may have a higher initial setup cost but offer better capacity and efficiency compared to traditional RDCs.

**RDC:** Resource Distribution Center

**CS:** Contactless Station

**AA:** Affected Area

![image](https://github.com/a868111817/Disaster-Relief-Logistics-Under-Covid-19-Delivery-Service/assets/49869328/91af44bb-5759-44e2-83bb-b9f41240340c)

Figure 1. Bozorgi-Amiri's General Resource Distribution Chain

## Problem Definition

Amiri's paper addresses the challenges of disaster planning and response while considering uncertainty in demand, supply, and cost resulting from the disaster. The model comprises three stages and two types of pair-wise transportation (Supplier-RDC and RDC-AA). With constraints on transportation and capacity limits in three sets of nodes, the primary goal is to determine the optimal number of commodities for delivery between nodes, identify locations for setting up RDCs, and specify capacity levels if an RDC is established. This optimization aims to minimize the total cost and the shortage cost in the least satisfied area.

However, we intend to make the following modifications to Bozorgi-Amiri's formulation while preserving the multi-objective (bi-objective) framework:

1. **Separation of RDCs:** We distinguish between standard RDCs (denoted as RDC) and Contactless Stations (CSs, denoted as CS).

2. **Separation of Affected Areas:** We categorize affected areas into high-risk and low-risk AAs. High-risk AAs only receive resources from CSs, while low-risk AAs can receive resources from both RDCs and CSs.

3. **Simplified Constraints:** We simplify the constraints by removing the procurement costs of commodities. Additionally, we fix the setup cost and capacity size for RDCs (Bozorgi-Amiri's paper features three setup costs with three sizes). We will manually determine a setup cost and capacity size for CSs.

In summary, our approach largely follows the formulation and multi-objective setting of Bozorgi-Amiri's paper, with the mentioned modifications to streamline the model and reduce complexity.

## Methodology

### Formulation

#### Sets and Indices

- $I$: Suppliers
- $J$: Candidate points for RDCs and CSs
- $K$: Affected Areas
- For each $j \in J$, it could be an RDC, a CS, or none (empty).
- $K'$: High-risk Affected Areas; only receive commodities from CSs.
- $K/K'$: Low-risk Affected Areas; receive commodities from both RDCs and CSs.
- $C$: Commodity Types.
- $S$: Possible scenarios (discrete).

#### Parameters

**Deterministic Parameters**

- $F^R$: Fixed setup cost for RDCs.
- $F^C$: Fixed setup cost for CSs.
- $C_{ijc}$: Transportation cost from supplier $i$ to candidate point $j$ with commodity $c$.
- $h_{kc}$: Inventory holding cost for commodity $c$ at AA $k$.
- $\pi_{c}$: Inventory shortage cost for commodity $c$.
- $v_{c}$: Required unit space for commodity $c$.
- $S_ic$: Amount of commodity $c$ supplied by supplier $i$.
- $M$: A large number.

**Stochastic Parameters**

- $p_s$: Occurrence probability of scenario $s \in S$.
- $C_{ijcs}$: Transportation cost from supplier $i$ to candidate point $j$ with commodity $c$ under scenario $s$.
- $C_{jkcs}$: Transportation cost from candidate point $j$ to AA $k$ with commodity $c$ under scenario $s$.
- $D_{kcs}$: Amount of demand for commodity $c$ under scenario $s$.
- $\rho_{jcs}$: Fraction of stocked materials of commodity $c$ remaining usable at candidate point $j$ under scenario $s$ ($0 \leq \rho_{jcs} \leq 1$).
- $\rho_{ics}$: Fraction of stocked materials of commodity $c$ remaining usable at supplier $i$ under scenario $s$ ($0 \leq \rho_{ics} \leq 1$).

#### Decision Variables

- $Q_{ijc}$: Amount of commodity $c$ supplied by supplier $i$, stored at candidate point $j$.
- $X_{ijcs}$: Amount of commodity $c$ transferred from supplier $i$ to candidate point $j$ under scenario $s$. If $X_{ijcs} > 0$, $j$ must be either an RDC or a CS.
- $Y_{jkcs}$: Amount of commodity $c$ transferred from candidate point $j$ to AA $k$ under scenario $s$. If $Y_{jkcs} > 0$, $j$ must be either an RDC or a CS.
- $I_{kcs}$: Amount of inventory of commodity $c$ held at AA $k$ under scenario $s$.
- $b_{kcs}$: Amount of shortage of commodity $c$ at AA $k$ under scenario $s$.
- $\alpha_i$: If candidate point $j$ is an RDC, $\alpha_j = 1$; otherwise, $=0$.
- $\beta_j$: If candidate point $j$ is a CS, $\beta_j = 1$; otherwise, $=0$.

#### Mathematical Formulations

These are defined for convenience and simplicity in objective functions.

- $\Sigma_{j \in J}(F^R\alpha_j + F^C\beta_j)$: (SC) Setup Cost for RDCs and CSs
- $\Sigma_{i\in I}\Sigma_{j \in J}\Sigma_{c \in C}C_{ijc}Q_{ijc}$: Transportation Cost from suppliers to RDCs and CSs (preparedness phase).
- $\Sigma_{i\in I}\Sigma_{j \in J}\Sigma_{c \in C}C_{ijcs}X_{ijcs}$: (TC-pre) Transportation Cost from suppliers to RDCs and CSs under a scenario (response phase).
- $\Sigma_{i\in I}\Sigma_{k \in K}\Sigma_{c \in C}C_{jkcs}Y_{jkcs}$: (TC-post) Transportation Cost from RDCs and CSs to AAs under a scenario (response phase).
- $\Sigma_{k \in k}\Sigma_{c \in C}h_{kc}I_{kcs}$: (IC) Inventory holding costs at AAs under a scenario (response phase).
- $\Sigma_{k \in K}\Sigma_{c \in C}\pi_{c}b_{kcs}$: (SHC) Shortage costs at AAs under a scenario (response phase).

## Constraints

The green parts are highlighted to indicate the revised parts from Bozorgi-Amiri's paper.

**(1) Control Balance Equation**: The amount of commodities sent from suppliers and other RDC/CS $j'$ to $j$ minus the amount $j$ sending out to other AA should roughly equal the amount of commodities transferred to AAs from the RDC $j$. If the left-hand side (LHS) is greater than the right-hand side (RHS), this inventory surplus is penalized by the first objective.

$$\Sigma_{i \in I} X_{ijcs} + \rho\Sigma_{i \in I}Q_{ijc} + \color{green}{\Sigma_{j' \neq j}{Y_{jj'cs}}\alpha_{j'}\beta_{j'}} - \Sigma_{k \in K}Y_{jkcs}(\alpha_j + \beta_j) = \delta_{jcs} \quad \forall j \in J, \forall c \in C, \forall s \in S$$

**(2) Inventory Equality Constraint**: The amount of commodities from RDC/CS $j$ to AA $k$ minus AA $k$'s demand should equal AA $k$'s inventory minus AA $k$'s shortage. The revised part covers the special case when $k$ is a special AA that can only receive commodities sent by a CS.

## Constraints

The green parts are highlighted to indicate the revised parts from Bozorgi-Amiri's paper.

**(3) RDC/CS Transferability**: RDCs/CSs can transfer commodities to other nodes only if there exists another RDC/CS/AA.

<!-- j is an RDC or a CS and k is a low-risk AA <=> j can send stuff to k -->
$$Y_{jkcs} \leq M(\alpha_j + \beta_j)D_{kcs} \quad \forall j \in J, \forall k \in K/K', \forall c \in C, \forall s \in S$$

<!-- j is a CS and k' is a high-risk AA <=> j can send commodities to k' -->
$$\color{green} Y_{jk'cs} \leq M\beta_jD_{k'cs} \quad \forall j \in J, \forall k' \in K', \forall c \in C, \forall s \in S$$

<!-- (28) -->
$$\Sigma_{i \in I} {X_{ijcs} \leq M(\alpha_j + \beta_j)} \quad \forall j \in J, \forall c \in C, \forall s \in S$$

**(5) RDC Capacity Constraint**: The amount of commodities sent from supplier $i$ to RDC $j$ should not exceed the capacity of the RDC. Similarly, the amount of commodities sent from supplier $i$ to CS $j$ should not exceed the capacity of the CS.

<!-- (30) -->
$$\Sigma_{i \in I}\Sigma_{c \in C} v_cQ_{ijc} \leq CapSize^R \cdot \alpha_j \quad \forall j \in J$$
$$\Sigma_{i \in I}\Sigma_{c \in C} v_cQ_{ijc} \leq CapSize^C \cdot \beta_j \quad \forall j \in J$$

**(6) Supplier Capacity Constraint (in preparedness phase)**: The amount of commodities a supplier sends out to other places should not exceed the supplier's own capacity (before the disaster).

<!-- (32) -->
$$\Sigma_{j \in J} Q_{ijc} \leq S_{ic} \quad \forall i \in I, \forall c \in C$$

**(7) Supplier Capacity Constraint (in response phase)**: The amount of commodities a supplier sends out to other places should not exceed the supplier's own capacity (after the disaster, under all scenarios).

<!-- (33) -->
$$\Sigma_{j \in J} X_{ijcs} \leq \rho_{ics} S_{ic} \quad \forall i \in I, \forall c \in C, \forall s \in S$$

**(8) RDC/CS Identity Constraint**: A node in set $J$ could only be (1) none, (2) an RDC, or (3) a CS, but not both an RDC and a CS simultaneously.

<!-- (34) -->
$$\alpha_j + \beta_j \leq 1 \quad \forall j \in J$$

**(9) CS Number Constraint**: $\epsilon$ is the maximum number of CSs allowed in the network.

$$\color{green} \Sigma_{j \in J} \beta_j \leq \epsilon$$

## Objectives

- **Objective 1**: Minimize the total costs
    $$SC + TC_{pre} + TC_{post}+ IC + SHC$$

    Sometimes the input parameters make the model infeasible, so we add a penalty term $\delta$ to penalize solutions that fail to meet the demand in a scenario or violate certain constraints while keeping the model feasible. The final objective 1 is:
    
    $$SC + TC_{pre} + TC_{post}+ IC + SHC + \gamma\Sigma_{j \in J}\Sigma_{c \in C}\Sigma_{s \in S}\delta_{jcs}$$

    Here, $\gamma$ is the penalty weight of the deviation term.

- **Objective 2**: Maximize the total satisfaction; i.e., minimize the shortage costs of the least satisfied AA under all scenarios.

    $$\Sigma_{s \in S}p_s(\Sigma_{c \in C}\max_{k \in K}{b_{kcs}})$$

### Multi-Objective Optimization

There are several methods to solve a multi-objective problem, as can be found in past literature (Mahjoob, M. and Abbasian, P., 2018; Kong, Z. Y., How, B. S., Mahmoud, A., & Sunarso, J., 2022; Yang, Z. et al., 2014). We employ the following two methods to combine our two objectives and solve the problem as a single-objective problem.

#### Weighted-Sum Method
Both objectives are assigned a positive weight ($w$ for $Obj_1$, $0 \leq w \leq 1$), and the goal is to minimize the weighted sum of both objective functions. An issue is that $Obj_1$ involves $Obj_2$, so it must be numerically greater than the latter. Therefore, assigning a small enough $w$ is important to avoid the dominance of the total cost over AA satisfaction.
$$\min wObj_1 + (1 - w)Obj_2$$

## Data Collection

We use the data from the case study in Bozorgi-Amiri's paper. The scenario is set in a well-populated region of Iran located near southern Central Alborz, with several active faults surrounding it (hence the disaster is imagined to be an earthquake).

1. $I$ contains 5 suppliers, including Sari, Qazvin, Tehran, Arak, and Isfahan.
2. $J$ contains 15 candidate nodes, including Gorgan, Semnan, Sari, Rasht, Qazvin, Karaj, Tehran, Varamin, Robat Karim, Islamshahr, Shahriar, Gom, Arak, Isfahan, and Kashan. Their pair-wise distance statistics are shown in figure 3. The setup costs of an RDC ($F^R$) and a CS ($F^C$) are shown in figure 3.
3. $K$ contains 15 demand points (AAs). The first 8 nodes are low-risk AAs, while the latter 7 are high-risk ones (the former is denoted $K/K'$, while the latter is denoted $K'$). Their demands under all scenarios ($D_{kcs}$) are shown in figure 4. The capacity of AA is an arbitrary value set to 16 (same unit as the capacity of an RDC and CS).
4. $C$ is the set of commodities; here, we use water, food, and shelter.
5. $S$ is the set of scenarios with occurrence probabilities $p_s = [0.45, 0.3, 0.1, 0.15]$.

## Result Analysis

![image_with_white_bg](https://github.com/a868111817/Disaster-Relief-Logistics-Under-Covid-19-Delivery-Service/assets/49869328/3f21147f-9397-4795-b609-cfa714b2a539)


### Table 1: Amount of Commodity Shipped from RDC to AA under Scenario
- Commodity water and food are shipped at 636 units per shipment.
- Commodity shelter is shipped at 184.24 units per shipment.
- Shelter appears to have higher transportation costs compared to the other two commodities.

## Conclusion

In this project, we proposed a multi-objective stochastic programming model to simultaneously optimize the humanitarian relief logistics. The model involves setting up contactless stations and using unmanned vehicles for specific needs. The model, solved as a single-objective mixed-integer problem using the Weighted-Sum method, includes a case study and weight analysis.

## Reference

[1] A multi-objective robust stochastic programming model for disaster relief logistics under uncertainty. Bozorgi-Amiri et al.
[2]  design of multimodal hub-and-spoke transportation network for emergency relief under COVID-19 pandemic: A meta-heuristic approach. Chi Li ,et al. 2023
[3] https://www.gurobi.com/documentation/9.1/refman/working_with_multiple_obje.html


