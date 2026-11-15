from src.meeting_ai import clean_transcript, result_to_csv, _normalize_result

def test_clean_transcript_normalizes_whitespace():
    assert clean_transcript("  Hello   team\r\n\r\n\r\nNext  ") == "Hello team\n\nNext"

def test_normalize_result_fills_missing_owner_and_deadline():
    result = _normalize_result({
        "summary": "Discussed launch.",
        "action_items": [{"task": "Send the plan"}]
    })
    assert result["action_items"][0]["owner"] == "Not specified"
    assert result["action_items"][0]["deadline"] == "Not specified"
    assert result["meeting_date"] == "Not specified"

def test_csv_contains_action_item_fields():
    csv_text = result_to_csv([{
        "task": "Send plan", "owner": "Maya", "deadline": "Friday",
        "status": "Open", "evidence": "Maya: I will send the plan."
    }])
    assert "task,owner,deadline,status,evidence" in csv_text
    assert "Send plan" in csv_text
