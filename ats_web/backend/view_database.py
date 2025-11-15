"""View and explore the feedback database"""

import json
from pathlib import Path
from datetime import datetime
from feedback_store import feedback_store

def print_separator(char="=", length=80):
    print(char * length)

def view_statistics():
    """View database statistics"""
    print_separator()
    print("FEEDBACK DATABASE STATISTICS")
    print_separator()
    
    stats = feedback_store.get_statistics()
    
    print(f"\n📊 Total Feedback Entries: {stats['total_feedback']}")
    print(f"⭐ Average Rating: {stats['average_rating']:.2f}/5.0")
    print(f"🗄️  ChromaDB Count: {stats['chromadb_count']}")
    print(f"🔍 FAISS Index Count: {stats['faiss_count']}")
    
    # Read JSONL for more details
    jsonl_file = Path("feedback_db/interactions.jsonl")
    if jsonl_file.exists():
        ratings_breakdown = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        types_count = {}
        
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line)
                rating = data['feedback']['rating']
                ratings_breakdown[rating] += 1
                
                # Count by type (from interaction_id)
                item_type = data['id'].split('_')[1] if '_' in data['id'] else 'chat'
                types_count[item_type] = types_count.get(item_type, 0) + 1
        
        print("\n📈 Rating Breakdown:")
        for rating in range(5, 0, -1):
            count = ratings_breakdown[rating]
            bar = "█" * count
            print(f"  {rating} ⭐: {bar} ({count})")
        
        print("\n📝 Feedback Types:")
        for item_type, count in sorted(types_count.items(), key=lambda x: x[1], reverse=True):
            print(f"  {item_type}: {count}")
    
    print_separator()

def view_recent_feedback(limit=10):
    """View recent feedback entries"""
    print_separator()
    print(f"RECENT FEEDBACK (Last {limit} entries)")
    print_separator()
    
    jsonl_file = Path("feedback_db/interactions.jsonl")
    if not jsonl_file.exists():
        print("\n❌ No feedback data found!")
        return
    
    # Read all entries
    entries = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            entries.append(json.loads(line))
    
    # Get last N entries
    recent = entries[-limit:] if len(entries) > limit else entries
    recent.reverse()  # Most recent first
    
    for i, entry in enumerate(recent, 1):
        print(f"\n[{i}] ID: {entry['id']}")
        print(f"    Timestamp: {entry['timestamp']}")
        print(f"    Rating: {'⭐' * entry['feedback']['rating']} ({entry['feedback']['rating']}/5)")
        print(f"    Query: {entry['query'][:80]}...")
        print(f"    Response: {entry['response'][:80]}...")
        
        if entry['feedback']['correct_points']:
            print(f"    ✅ Correct: {', '.join(entry['feedback']['correct_points'][:3])}")
        if entry['feedback']['incorrect_points']:
            print(f"    ❌ Incorrect: {', '.join(entry['feedback']['incorrect_points'][:3])}")
    
    print_separator()

def view_high_quality_samples(min_rating=4, limit=10):
    """View high-quality feedback samples"""
    print_separator()
    print(f"HIGH-QUALITY SAMPLES (Rating >= {min_rating})")
    print_separator()
    
    jsonl_file = Path("feedback_db/interactions.jsonl")
    if not jsonl_file.exists():
        print("\n❌ No feedback data found!")
        return
    
    high_quality = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data['feedback']['rating'] >= min_rating:
                high_quality.append(data)
    
    if not high_quality:
        print(f"\n❌ No feedback with rating >= {min_rating} found!")
        return
    
    print(f"\nFound {len(high_quality)} high-quality samples\n")
    
    for i, entry in enumerate(high_quality[:limit], 1):
        print(f"[{i}] Rating: {'⭐' * entry['feedback']['rating']}")
        print(f"    Query: {entry['query']}")
        print(f"    Response: {entry['response'][:150]}...")
        if entry['feedback']['correct_points']:
            print(f"    ✅ {', '.join(entry['feedback']['correct_points'])}")
        print()
    
    print_separator()

def view_low_quality_samples(max_rating=2, limit=10):
    """View low-quality feedback samples that need correction"""
    print_separator()
    print(f"LOW-QUALITY SAMPLES (Rating <= {max_rating}) - Need Improvement")
    print_separator()
    
    jsonl_file = Path("feedback_db/interactions.jsonl")
    if not jsonl_file.exists():
        print("\n❌ No feedback data found!")
        return
    
    low_quality = []
    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            if data['feedback']['rating'] <= max_rating:
                low_quality.append(data)
    
    if not low_quality:
        print(f"\n❌ No feedback with rating <= {max_rating} found!")
        return
    
    print(f"\nFound {len(low_quality)} samples needing improvement\n")
    
    for i, entry in enumerate(low_quality[:limit], 1):
        print(f"[{i}] Rating: {'⭐' * entry['feedback']['rating']}")
        print(f"    Query: {entry['query']}")
        print(f"    Original Response: {entry['response'][:100]}...")
        if entry['feedback']['incorrect_points']:
            print(f"    ❌ Issues: {', '.join(entry['feedback']['incorrect_points'])}")
        if entry['feedback']['ideal_response'] != entry['response']:
            print(f"    ✅ Ideal: {entry['feedback']['ideal_response'][:100]}...")
        print()
    
    print_separator()

def search_feedback(query_text, n_results=5):
    """Search for similar feedback"""
    print_separator()
    print(f"SEARCH RESULTS FOR: '{query_text}'")
    print_separator()
    
    results = feedback_store.search_similar_chromadb(query_text, n_results)
    
    if 'error' in results:
        print(f"\n❌ Error: {results['error']}")
        print("Make sure ChromaDB is installed: pip install chromadb")
        return
    
    if not results.get('documents') or not results['documents'][0]:
        print("\n❌ No results found!")
        return
    
    print(f"\nFound {len(results['documents'][0])} similar entries:\n")
    
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        print(f"[{i}] Similarity: {1 - distance:.2%}")
        print(f"    Rating: {'⭐' * metadata['rating']}")
        print(f"    Query: {metadata['query'][:80]}...")
        print(f"    Response: {metadata['response'][:80]}...")
        print()
    
    print_separator()

def export_to_csv():
    """Export feedback to CSV for Excel/analysis"""
    import csv
    
    jsonl_file = Path("feedback_db/interactions.jsonl")
    if not jsonl_file.exists():
        print("❌ No feedback data found!")
        return
    
    csv_file = Path("feedback_db/feedback_export.csv")
    
    with open(jsonl_file, 'r', encoding='utf-8') as f_in:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerow([
                'ID', 'Timestamp', 'Rating', 'Query', 'Response',
                'Correct Points', 'Incorrect Points', 'Missing Points', 'Ideal Response'
            ])
            
            for line in f_in:
                data = json.loads(line)
                writer.writerow([
                    data['id'],
                    data['timestamp'],
                    data['feedback']['rating'],
                    data['query'],
                    data['response'],
                    ', '.join(data['feedback']['correct_points']),
                    ', '.join(data['feedback']['incorrect_points']),
                    ', '.join(data['feedback'].get('missing_points', [])),
                    data['feedback']['ideal_response']
                ])
    
    print(f"✅ Exported to: {csv_file.absolute()}")
    print("   You can open this in Excel or Google Sheets!")

def main():
    """Main menu"""
    while True:
        print("\n" + "="*80)
        print("FEEDBACK DATABASE VIEWER")
        print("="*80)
        print("\n1. View Statistics")
        print("2. View Recent Feedback (last 10)")
        print("3. View High-Quality Samples (rating >= 4)")
        print("4. View Low-Quality Samples (rating <= 2)")
        print("5. Search Feedback")
        print("6. Export to CSV")
        print("7. View All Feedback (last 20)")
        print("0. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            view_statistics()
        elif choice == "2":
            view_recent_feedback(10)
        elif choice == "3":
            view_high_quality_samples(4, 10)
        elif choice == "4":
            view_low_quality_samples(2, 10)
        elif choice == "5":
            query = input("Enter search query: ").strip()
            if query:
                search_feedback(query, 5)
        elif choice == "6":
            export_to_csv()
        elif choice == "7":
            view_recent_feedback(20)
        elif choice == "0":
            print("\nGoodbye! 👋")
            break
        else:
            print("\n❌ Invalid choice!")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
