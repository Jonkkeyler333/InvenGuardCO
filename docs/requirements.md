<div align="center">

# InvenGuardCO : Requirements

[Back to Analysis](analysis.md)

</div>

## Functional Requirements

<details open>
<summary><strong>FR-01 · Inventory Management</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall allow users to record material entries and update the inventory in real time for manual inventory movements such as entries and adjustments. |
| **Acceptance Criteria** | Given a material entry or adjustment, when a user records it, then the system shall update the inventory levels accordingly. |

</details>

<details>
<summary><strong>FR-02 · Bill of Materials (BOM) Management</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall allow users to define production recipes that specify the required quantities of raw materials per finished product. |
| **Acceptance Criteria** | Given a new product, when a user creates a BOM, then the system shall store the required raw materials and their quantities for that product. |

</details>

<details>
<summary><strong>FR-03 · Production Feasibility Validation</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall validate, given a production order, whether it can be executed with the currently available inventory before committing any stock changes, relying on the BOM of each product in the order. |
| **Acceptance Criteria** | Given a production order, when a user attempts to execute it, then the system shall check if sufficient raw materials are available and either approve or reject the order based on inventory levels. |

</details>

<details>
<summary><strong>FR-04 · Automated Inventory Updates</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall automatically register material consumption and update inventory records consistently upon production execution. |
| **Acceptance Criteria** | Given a production order execution, when the order is completed, then the system shall deduct the consumed raw materials from the inventory based on the BOM. |

</details>

<details>
<summary><strong>FR-05 · Low-Stock Alerts</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall generate alerts when inventory levels fall below predefined thresholds. |
| **Acceptance Criteria** | Given a material's inventory level, when it falls below the defined threshold, then the system shall notify the relevant users about the low-stock situation. |

</details>

<details>
<summary><strong>FR-06 · Production Order Management</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall allow users to create, manage, and monitor production orders. |
| **Acceptance Criteria** | Given a production order, when a user creates or updates it, then the system shall store the order details and provide status updates during its execution. |

</details>

<details>
<summary><strong>FR-07 · User Management</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall allow the Plant Manager (admin) to create and manage users with different roles and permissions. |
| **Acceptance Criteria** | Given a user management request, when the Plant Manager creates or updates a user, then the system shall store the user details and assign the appropriate role and permissions. |

</details>

<details>
<summary><strong>FR-08 · Reporting</strong></summary>

| | |
|---|---|
| **Priority** | ![Should Have](https://img.shields.io/badge/Should%20Have-yellow) |
| **Description** | The system shall provide reporting capabilities to analyze inventory levels, production efficiency, and material consumption trends. |
| **Acceptance Criteria** | Given a reporting request, when a user generates a report, then the system shall compile the relevant data and present it in a user-friendly format. |

</details>

---

## Non-Functional Requirements

<details open>
<summary><strong>NFR-01 · Concurrency</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | The system shall support multiple users performing operations simultaneously without data conflicts. |
| **Acceptance Criteria** | Given multiple users accessing the system, when they perform operations concurrently (e.g., create production orders with similar raw materials), then the system shall maintain data integrity and consistency. |

</details>

<details>
<summary><strong>NFR-02 · Transactional Integrity</strong></summary>

| | |
|---|---|
| **Priority** | ![Must Have](https://img.shields.io/badge/Must%20Have-critical) |
| **Description** | All inventory deductions during production execution shall be atomic. |
| **Acceptance Criteria** | Given a production order with 5 materials, when one deduction fails, then all changes shall roll back and inventory shall remain unchanged. |

</details>

<details>
<summary><strong>NFR-03 · Alert Delivery</strong></summary>

| | |
|---|---|
| **Priority** | ![Should Have](https://img.shields.io/badge/Should%20Have-yellow) |
| **Description** | Low-stock alerts shall be delivered within 30 seconds of threshold breach via in-app notification. |
| **Acceptance Criteria** | Given inventory dropping below threshold, when the event is detected, then relevant users shall receive a notification within 30 seconds. |

</details>