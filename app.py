from flask import Flask, render_template, request, redirect, url_for
from datetime import date

app = Flask(__name__)

# 課程清單：這裡的 time 是「時間點」，日期由學生選
classes = [
    {"id": 1, "name": "核心訓練", "coach": "A教練", "time": "18:00"},
    {"id": 2, "name": "臀腿訓練", "coach": "B教練", "time": "20:00"},
    {"id": 3, "name": "伸展課", "coach": "A教練", "time": "19:00"},
]

# 用來暫存預約資料（程式重啟就會清空）
# 每筆資料：class_id, student name, date(字串)
booked = []


@app.route("/")
def index():
    # 今天日期，給前端當預設值
    today = date.today().isoformat()  # 例如 2025-12-01
    return render_template("index.html", classes=classes, today=today)


@app.route("/book", methods=["POST"])
def book():
    class_id = int(request.form["class_id"])
    name = request.form["name"].strip()
    selected_date = request.form["date"]  # 從表單取得日期字串，例如 "2025-12-10"

    # 儲存預約資料
    booked.append({"class_id": class_id, "name": name, "date": selected_date})

    # 也印在後台 console（Anaconda 視窗）方便你看
    print("===== 新預約 =====")
    print(f"姓名：{name}")
    print(f"課程 ID：{class_id}")
    print(f"日期：{selected_date}")
    print("=================")

    # 預約後回首頁
    return redirect(url_for("index"))


@app.route("/secret-admin-only")
def admin():
    """簡易後台：顯示所有預約資料"""
    enriched = []
    for b in booked:
        cls = next((c for c in classes if c["id"] == b["class_id"]), None)
        enriched.append(
            {
                "student": b["name"],
                "class_name": cls["name"] if cls else "未知課程",
                "coach": cls["coach"] if cls else "",
                "time": cls["time"] if cls else "",
                "date": b["date"],  # 學生選的日期
            }
        )

    return render_template("admin.html", bookings=enriched)


if __name__ == "__main__":
    app.run(debug=True)
