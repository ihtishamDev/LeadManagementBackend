from fastapi import APIRouter, HTTPException
from db.database import get_connection
from schema.schema import AddLead

router = APIRouter(prefix="/leads", tags=["Leads"])


def generate_lead_id(cursor):
    query = """
    SELECT MAX(num) AS max_id
    FROM (
        SELECT CAST(SUBSTRING(id, 3) AS UNSIGNED) AS num FROM leads
        UNION ALL
        SELECT CAST(SUBSTRING(id, 3) AS UNSIGNED) AS num FROM customers
    ) AS all_ids
    """
    cursor.execute(query)
    result = cursor.fetchone()

    max_id = result[0] if result and result[0] is not None else 0
    next_id = max_id + 1

    return f"L-{next_id:03d}"


@router.post("/")
def create_lead(lead: AddLead):
    conn = get_connection()
    cursor = conn.cursor()

    lead_id = generate_lead_id(cursor)

    query = """
    INSERT INTO leads
    (id, Name, PhoneNumber, Email, Source, Status, Budget, Notes)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        lead_id,
        lead.name,
        lead.phone,
        lead.email,
        lead.source,
        lead.status,
        lead.budget,
        lead.notes,
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Lead created", "leadId": lead_id}


@router.get("/")
def get_leads():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM leads ORDER BY CAST(SUBSTRING(id, 3) AS UNSIGNED) ASC")
    leads = cursor.fetchall()

    transformed = []
    for row in leads:
        transformed.append({
            "leadId": row.get("id"),
            "id": row.get("id"),
            "name": row.get("Name"),
            "Name": row.get("Name"),
            "phone": row.get("PhoneNumber"),
            "PhoneNumber": row.get("PhoneNumber"),
            "email": row.get("Email"),
            "Email": row.get("Email"),
            "source": row.get("Source"),
            "Source": row.get("Source"),
            "status": row.get("Status"),
            "Status": row.get("Status"),
            "budget": row.get("Budget"),
            "Budget": row.get("Budget"),
            "notes": row.get("Notes"),
            "Notes": row.get("Notes"),
        })

    cursor.close()
    conn.close()

    return transformed


@router.put("/{lead_id}")
def update_lead(lead_id: str, lead: AddLead):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    UPDATE leads
    SET Name=%s, PhoneNumber=%s, Email=%s,
        Source=%s, Status=%s, Budget=%s, Notes=%s
    WHERE id=%s
    """

    values = (
        lead.name,
        lead.phone,
        lead.email,
        lead.source,
        lead.status,
        lead.budget,
        lead.notes,
        lead_id,
    )

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Lead updated"}


@router.delete("/{lead_id}")
def delete_lead(lead_id: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM leads WHERE id=%s", (lead_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Lead deleted"}


@router.post("/{lead_id}/convert")
def convert_lead_to_customer(lead_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM leads WHERE id=%s", (lead_id,))
    lead = cursor.fetchone()

    if not lead:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Lead not found")

    cursor.execute("SELECT id FROM customers WHERE id=%s", (lead_id,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        cursor.close()
        conn.close()
        raise HTTPException(
            status_code=400,
            detail=f"Customer with ID {lead_id} already exists"
        )

    insert_query = """
    INSERT INTO customers
    (id, Name, PhoneNumber, Email, Source, Budget, Notes)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        lead["id"],
        lead["Name"],
        lead["PhoneNumber"],
        lead["Email"],
        lead["Source"],
        lead["Budget"],
        lead["Notes"],
    )

    cursor.execute(insert_query, values)
    cursor.execute("DELETE FROM leads WHERE id=%s", (lead_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return {"message": "Lead converted to customer"}