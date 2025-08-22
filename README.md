# 👆 Order-Driven-Scheduling-MILP-Optimizer-using-Python
This MILP optimizer demonstrates how to compute an **order-drive production schedule** accounting for **priorities, due dates, and penalties** and provides a base for dynamic re-scheduling

---

## 🧏 Problem Context
In **Make-To-Order** and **Custom production environments**, the schedule is often disrupted by **last-minute high-priority (rush) orders**. We must dynamically trade off:
- **Due dates** (to minimize total tardiness or lateness penalties),
- **Rush-order-priorities**, and
- **Sequence-depenedent setup costs**

---

## 💇 Model features
- Machines: parallel identical machines
- Orders: multiple orders, each with:
   - Processing time,
   - Due date,
   - Priority weight,
   - Setup time (if preceding order differs).
- *Decision variables*:
   - Sequencing of orders (start/finish times),
   - Assignment to machines,
   - Order lateness/tardiness

- Objective: **Minimise weighted tardiness + Setup costs** 
