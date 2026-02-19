
# Star Schema (Vendas)
```mermaid
erDiagram
  FACT_ORDERS ||--o{ DIM_CUSTOMER : has
  FACT_ORDERS {
    string order_id
    date order_date
    decimal total_amount
    string customer_id
  }
  DIM_CUSTOMER {
    string customer_id
    string customer_name
  }
```
