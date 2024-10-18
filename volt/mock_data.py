mock_alation_data = {
  "CCcustomer": {
    "columns": [
      {
        "name": "customer_id",
        "data_type": "INT",
        "description": "Unique identifier for each customer (Primary Key)."
      },
      {
        "name": "first_name",
        "data_type": "VARCHAR(50)",
        "description": "Customer’s first name."
      },
      {
        "name": "last_name",
        "data_type": "VARCHAR(50)",
        "description": "Customer’s last name."
      },
      {
        "name": "date_of_birth",
        "data_type": "DATE",
        "description": "Customer’s date of birth."
      },
      {
        "name": "email",
        "data_type": "VARCHAR(100)",
        "description": "Customer’s email address."
      },
      {
        "name": "phone_number",
        "data_type": "VARCHAR(20)",
        "description": "Customer’s phone number."
      },
      {
        "name": "address",
        "data_type": "VARCHAR(255)",
        "description": "Customer’s physical address (street, city, state, postal code)."
      },
      {
        "name": "account_status",
        "data_type": "VARCHAR(20)",
        "description": "Status of the customer’s account (e.g., Active, Closed, Suspended)."
      },
      {
        "name": "current_balance",
        "data_type": "DECIMAL(10, 2)",
        "description": "The current outstanding balance on the customer’s credit card."
      },
      {
        "name": "payment_due_date",
        "data_type": "DATE",
        "description": "Date when the next payment is due."
      },
         {
        "name": "total_credit_limit",
        "data_type": "DECIMAL(10, 2)",
        "description": "Maximum credit limit granted to the customer."
      },
      {
        "name": "reward_points",
        "data_type": "INT",
        "description": "Total reward points the customer has accumulated (if applicable)."
      }
    ]
  }
}

mock_sharepoint_data={
  "CreditCardRewardsProgram": {
    "results": [
      {
        "link": "https://www.discoversharepoint.com/rewards-overview",
        "description": "Learn about the different rewards programs available for credit cardholders, including cashback, points, and travel rewards."
      },
      {
        "link": "https://www.discoversharepoint.com/maximize-rewards",
        "description": "Tips and strategies for earning the maximum rewards on your credit card spend, including bonus categories and promotions."
      },
      {
        "link": "https://www.discoversharepoint.com/premium-rewards",
        "description": "Discover the exclusive rewards and benefits available to premium credit cardholders, including luxury travel and dining experiences."
      }
    ]
  }
}

mock_retriever_data = """Discover Financial Services is a financial services company primarily known for its credit card products and banking services. Here are some key points about the company:

1. **Credit Cards**: Discover is well-known for its credit card offerings, which include cash back, travel rewards, and student credit cards. The Discover it® card is particularly popular for its cashback rewards program.

2. **Banking Services**: In addition to credit cards, Discover also offers various banking services, including savings accounts, money market accounts, and certificates of deposit (CDs).

3. **Rewards Programs**: Discover cards typically offer cashback rewards with various bonus categories that change throughout the year, allowing cardholders to earn extra rewards on specific types of purchases.

If you have any specific questions or need more information about Discover Financial Services, feel free to ask!"""
