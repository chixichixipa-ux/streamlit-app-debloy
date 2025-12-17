from datetime import datetime, timedelta

# 定数定義
MAX_BORROW_LIMIT = 5  # 会員の最大貸出可能冊数
BORROW_PERIOD_DAYS = 14  # 貸出期間（日数）
FINE_PER_DAY = 100  # 1日あたりの延滞料金（円）

# データストア
books = []
members = []
borrow_records = []


# ヘルパー関数
def find_book(book_id):
    """図書IDから図書を検索する"""
    for book in books:
        if book["book_id"] == book_id:
            return book
    return None


def find_member(member_id):
    """会員IDから会員を検索する"""
    for member in members:
        if member["member_id"] == member_id:
            return member
    return None


def count_member_borrowed_books(member_id):
    """会員が現在借りている冊数をカウントする"""
    count = 0
    for record in borrow_records:
        if record["member_id"] == member_id and not record["returned"]:
            count += 1
    return count

# 図書管理関数
def add_book(book_id, title, author, copies):
    """図書を追加する"""
    if find_book(book_id):
        print(f"図書ID「{book_id}」の本は既に存在します。")
        return

    books.append({
        "book_id": book_id,
        "title": title,
        "author": author,
        "copies": copies,
        "available_copies": copies
    })
    print(f"図書「{title}」（ID: {book_id}, 著者: {author}, 冊数: {copies}）を追加しました。")

def list_books():
    """すべての図書を一覧表示する"""
    if not books:
        print("現在、登録されている図書はありません。")
        return

    print("\n--- 図書一覧 ---")
    for book in books:
        print(f"ID: {book['book_id']}, タイトル: {book['title']}, "
              f"著者: {book['author']}, 総冊数: {book['copies']}, "
              f"在庫: {book['available_copies']}")

def search_book(book_id):
    """図書IDで図書を検索する"""
    book = find_book(book_id)
    if book:
        print(f"\nID: {book['book_id']}, タイトル: {book['title']}, "
              f"著者: {book['author']}, 総冊数: {book['copies']}, "
              f"在庫: {book['available_copies']}")
    else:
        print(f"図書ID「{book_id}」の本は存在しません。")

# 会員管理関数
def add_member(member_id, name):
    """会員を追加する"""
    if find_member(member_id):
        print(f"会員ID「{member_id}」の会員は既に存在します。")
        return

    members.append({"member_id": member_id, "name": name})
    print(f"会員「{name}」（ID: {member_id}）を追加しました。")

def list_members():
    """すべての会員を一覧表示する"""
    if not members:
        print("現在、登録されている会員はいません。")
        return

    print("\n--- 会員一覧 ---")
    for member in members:
        borrowed_count = count_member_borrowed_books(member['member_id'])
        print(f"ID: {member['member_id']}, 名前: {member['name']}, "
              f"借りている冊数: {borrowed_count}")

# 貸出・返却関数
def borrow_book(book_id, member_id):
    """図書を貸し出す"""
    book = find_book(book_id)
    if not book:
        print(f"図書ID「{book_id}」の本は存在しません。")
        return

    member = find_member(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return

    if book["available_copies"] <= 0:
        print(f"図書「{book['title']}」は現在貸出可能な冊数がありません。")
        return

    borrowed_count = count_member_borrowed_books(member_id)
    if borrowed_count >= MAX_BORROW_LIMIT:
        print(f"貸出可能数は{MAX_BORROW_LIMIT}冊までです。")
        return

    # 現在の日付から貸出日と返却期限を計算
    today = datetime.now()
    borrow_date = today.strftime("%Y-%m-%d")
    due_date = (today + timedelta(days=BORROW_PERIOD_DAYS)).strftime("%Y-%m-%d")

    borrow_records.append({
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": borrow_date,
        "due_date": due_date,
        "returned": False
    })
    book["available_copies"] -= 1
    
    print(f"図書「{book['title']}」を会員「{member['name']}」に貸し出しました。")
    print(f"返却期限: {due_date}")

def list_borrowed_books():
    """貸出中の図書を一覧表示する"""
    print("\n--- 貸出中の図書一覧 ---")
    borrow_count = 0
    
    for record in borrow_records:
        if not record["returned"]:
            book = find_book(record["book_id"])
            member = find_member(record["member_id"])
            
            if book and member:
                print(f"図書: {book['title']}（ID: {record['book_id']}）, "
                      f"会員: {member['name']}（ID: {record['member_id']}）, "
                      f"貸出日: {record['borrow_date']}, 返却期限: {record['due_date']}")
                borrow_count += 1
    
    if borrow_count == 0:
        print("現在、貸出中の図書はありません。")

def return_book(book_id, member_id):
    """図書を返却する"""
    record_found = None
    
    for record in borrow_records:
        if (record["book_id"] == book_id and 
            record["member_id"] == member_id and 
            not record["returned"]):
            record["returned"] = True
            record_found = record
            break
    
    if not record_found:
        print(f"図書ID「{book_id}」を会員ID「{member_id}」の会員は借りていません。")
        return

    book = find_book(book_id)
    if book:
        book["available_copies"] += 1
        print(f"図書「{book['title']}」が返却されました。")
    else:
        print(f"図書ID「{book_id}」の本は存在しません。")

# 延滞料金計算関数
def calculate_fines():
    """延滞料金を計算して表示する"""
    print("\n--- 延滞料金一覧 ---")
    fine_count = 0
    today = datetime.now()
    
    for record in borrow_records:
        if not record["returned"]:
            book = find_book(record["book_id"])
            member = find_member(record["member_id"])
            
            if book and member:
                due_date = datetime.strptime(record["due_date"], "%Y-%m-%d")
                overdue_days = max((today - due_date).days, 0)
                fine = overdue_days * FINE_PER_DAY
                
                if overdue_days > 0:
                    print(f"図書: {book['title']}（ID: {record['book_id']}）, "
                          f"会員: {member['name']}（ID: {record['member_id']}）, "
                          f"延滞日数: {overdue_days}日, 延滞料金: {fine}円")
                    fine_count += 1
    
    if fine_count == 0:
        print("現在、延滞している図書はありません。")

def show_member_borrowed_books(member_id):
    """会員が借りている図書を表示する"""
    member = find_member(member_id)
    if not member:
        print(f"会員ID「{member_id}」の会員は存在しません。")
        return

    print(f"\n--- 会員「{member['name']}」の借りている図書 ---")
    borrow_count = 0
    
    for record in borrow_records:
        if record["member_id"] == member_id and not record["returned"]:
            book = find_book(record["book_id"])
            if book:
                print(f"図書: {book['title']}（ID: {record['book_id']}）, "
                      f"著者: {book['author']}, 貸出日: {record['borrow_date']}, "
                      f"返却期限: {record['due_date']}")
                borrow_count += 1
    
    if borrow_count == 0:
        print(f"会員「{member['name']}」は現在、図書を借りていません。")

# メイン関数
def main():
    """メインメニューを表示してユーザー操作を処理する"""
    while True:
        print("\n" + "="*50)
        print("図書館管理システムメニュー")
        print("="*50)
        print("1: 図書を追加")
        print("2: 図書一覧を表示")
        print("3: 図書を検索")
        print("4: 会員を追加")
        print("5: 会員一覧を表示")
        print("6: 図書を貸し出す")
        print("7: 貸出中の図書一覧を表示")
        print("8: 図書を返却")
        print("9: 延滞料金を計算")
        print("10: 会員の借りている図書を表示")
        print("11: 終了")
        print("="*50)

        try:
            choice = int(input("\n操作を選択してください（1-11）: "))

            if choice == 1:
                book_id = input("図書IDを入力してください: ")
                title = input("タイトルを入力してください: ")
                author = input("著者名を入力してください: ")
                copies = int(input("冊数を入力してください: "))
                add_book(book_id, title, author, copies)

            elif choice == 2:
                list_books()

            elif choice == 3:
                book_id = input("検索する図書IDを入力してください: ")
                search_book(book_id)

            elif choice == 4:
                member_id = input("会員IDを入力してください: ")
                name = input("名前を入力してください: ")
                add_member(member_id, name)

            elif choice == 5:
                list_members()

            elif choice == 6:
                book_id = input("貸し出す図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                borrow_book(book_id, member_id)

            elif choice == 7:
                list_borrowed_books()

            elif choice == 8:
                book_id = input("返却する図書IDを入力してください: ")
                member_id = input("会員IDを入力してください: ")
                return_book(book_id, member_id)

            elif choice == 9:
                calculate_fines()

            elif choice == 10:
                member_id = input("会員IDを入力してください: ")
                show_member_borrowed_books(member_id)

            elif choice == 11:
                print("図書館管理システムを終了します。")
                break

            else:
                print("無効な選択です。1-11の数字を入力してください。")

        except ValueError:
            print("\n入力エラー: 数値を正しく入力してください。")
        except KeyboardInterrupt:
            print("\n\n操作がキャンセルされました。")
            break
        except Exception as e:
            print(f"\n予期しないエラーが発生しました: {e}")


if __name__ == "__main__":
    print("\n図書館管理システムを起動しています...")
    main()
    print("\nシステムを終了しました。ご利用ありがとうございました。")