# Table initialization code node for n8n
# This creates session-based tables if they don't exist
# Requires PostgreSQL connection configured in n8n

results = []

for item in _input.all():
    try:
        # Get session_id from the input (usually Telegram user_id)
        session_id = None
        
        # Try different possible sources for session_id
        if "session_id" in item.json:
            session_id = item.json["session_id"]
        elif "user_id" in item.json:
            session_id = item.json["user_id"]
        elif "message" in item.json and "from" in item.json["message"] and "id" in item.json["message"]["from"]:
            session_id = item.json["message"]["from"]["id"]
        elif "from" in item.json and "id" in item.json["from"]:
            session_id = item.json["from"]["id"]
        
        if not session_id:
            raise ValueError("No session_id or user_id found in input")
        
        # Generate table creation queries with the actual session_id
        receipts_table = f"receipts_{session_id}"
        items_table = f"receipt_items_{session_id}"
        
        # SQL queries to create tables if they don't exist
        create_receipts_table = f"""
        CREATE TABLE IF NOT EXISTS public.{receipts_table} (
            id SERIAL PRIMARY KEY,
            business_name VARCHAR(255) NOT NULL,
            business_address TEXT,
            business_tax_id VARCHAR(50),
            receipt_number VARCHAR(100),
            receipt_date TIMESTAMP NOT NULL,
            payment_method VARCHAR(50),
            tax_amount DECIMAL(10,2),
            total_amount DECIMAL(10,2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        create_items_table = f"""
        CREATE TABLE IF NOT EXISTS public.{items_table} (
            id SERIAL PRIMARY KEY,
            receipt_id INTEGER NOT NULL,
            product_name VARCHAR(255) NOT NULL,
            product_code VARCHAR(100),
            category VARCHAR(100),
            quantity DECIMAL(10,3) NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            tax_rate DECIMAL(5,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (receipt_id) REFERENCES public.{receipts_table}(id) ON DELETE CASCADE
        );
        """
        
        # Create indexes for better performance
        create_indexes = f"""
        CREATE INDEX IF NOT EXISTS idx_{receipts_table}_date ON public.{receipts_table}(receipt_date);
        CREATE INDEX IF NOT EXISTS idx_{receipts_table}_business ON public.{receipts_table}(business_name);
        CREATE INDEX IF NOT EXISTS idx_{items_table}_receipt_id ON public.{items_table}(receipt_id);
        CREATE INDEX IF NOT EXISTS idx_{items_table}_product ON public.{items_table}(product_name);
        """
        
        # Combine all queries
        full_query = create_receipts_table + create_items_table + create_indexes
        
        results.append({
            "json": {
                "success": True,
                "session_id": session_id,
                "receipts_table": receipts_table,
                "items_table": items_table,
                "sql_query": full_query.strip(),
                "message": f"Tables initialized for session {session_id}"
            }
        })
        
    except Exception as e:
        results.append({
            "json": {
                "success": False,
                "error": str(e),
                "sql_query": None,
                "message": f"Error initializing tables: {str(e)}"
            }
        })

return results