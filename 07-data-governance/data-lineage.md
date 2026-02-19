
# Data Lineage (Visão)
```mermaid
flowchart LR
  MySQL --> Bronze_Customers --> Silver_Customers --> Gold_FactOrders
  DB2   --> Bronze_Ledger    --> Silver_Ledger    --> Gold_FactOrders
  FTP   --> Bronze_Shipments --> Silver_Shipments
```
