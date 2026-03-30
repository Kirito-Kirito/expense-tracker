import io
import os
from django.http import FileResponse
from django.template import loader
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import date, datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Expense
from .forms import ExpenseForm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4


# Create your views here.
FONT_PATH = os.path.join(os.path.dirname(__file__), "fonts/MSGOTHIC.TTC")

pdfmetrics.registerFont(TTFont("MSGothic", FONT_PATH))


def expense_list(request):

    today = date.today()
    selected_month = int(request.GET.get("month", today.month))
    selected_year = int(request.GET.get("year", today.year))

    expenses = Expense.objects.filter(
        date__month=selected_month, date__year=selected_year
    ).order_by("date")
    current_total = expenses.aggregate(Sum("amount"))["amount__sum"] or 0
    current_month_first_day = date(selected_year, selected_month, 1)
    current_month_name = f"{selected_month}月"

    prev_month_date = current_month_first_day - timedelta(days=1)
    prev_month_name = f"{prev_month_date.month}月"
    prev_total = (
        Expense.objects.filter(
            date__month=prev_month_date.month, date__year=prev_month_date.year
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )

    difference = current_total - prev_total

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm()

    context = {
        "expenses": expenses,
        "form": form,
        "total": current_total,
        "prev_total": prev_total,
        "difference": difference,
        "abs_difference": abs(difference),
        "current_month": selected_month,
        "current_year": selected_year,
        "prev_month_name": prev_month_name,
        "current_month_name": current_month_name,
        "months": range(1, 13),
        "years": range(today.year - 2, today.year + 2),
    }
    return render(request, "expenses_list.html", context)


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    expense.delete()
    return redirect("expense_list")


def edit_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect("expense_list")
    else:
        form = ExpenseForm(instance=expense)

    return render(request, "edit_expenses.html", {"form": form})


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = os.path.join(BASE_DIR, "monthly_transport_expense", "fonts", "MSGOTHIC.TTC")

pdfmetrics.registerFont(TTFont("MSGothic", FONT_PATH))


def export_expenses_pdf(request):
    today = datetime.now()
    month = int(request.GET.get("month", today.month))
    year = int(request.GET.get("year", today.year))

    buffer = io.BytesIO()
    # PDF margin တွေကို သတ်မှတ်မယ်
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottomMargin=18,
    )
    elements = []

    styles = getSampleStyleSheet()

    title_text = f"<b>交通費申請書 ({year}年{month}月分)</b>"

    title_style = ParagraphStyle(
        name="Title_JA",
        parent=styles["Title"],
        fontName="MSGothic",
        fontSize=20,
        alignment=TA_CENTER,
        leading=24,
        spaceAfter=30,
    )

    elements.append(Paragraph(title_text, title_style))

    sub_text_style = ParagraphStyle(
        name="SubText",
        parent=styles["Normal"],
        fontName="MSGothic",
        fontSize=9,
        alignment=TA_LEFT,
        spaceAfter=20,
    )
    elements.append(
        Paragraph("以下のとおり、交通費の申請をいたします。", sub_text_style)
    )

    display_name = "ゼイーヤーリン"

    stamp_cell = Table(
        [
            ["確認印"],
            [""],
        ],
        colWidths=[60],
        rowHeights=[15, 45],
    )

    stamp_cell.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "MSGothic"),
                ("FONTSIZE", (0, 0), (0, 0), 8),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.black),  # ဘောင်ကွက်ဆွဲမယ်
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    colors.lightgrey,
                ),  # '確認印' ကို အရောင်ခြယ်မယ်
            ]
        )
    )

    company_info = [
        ["", "ジービー 株式会社"],
        ["", "未来ストーリー 株式会社"],
        ["氏名:", display_name],
    ]

    info_table = Table(company_info, colWidths=[30, 200])
    info_table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), "MSGothic"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 2), (1, 2), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LINEBELOW", (1, 2), (1, 2), 0.4, colors.black),
            ]
        )
    )

    header_table = Table([[info_table, "", stamp_cell]], colWidths=[350, 80, 70])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (2, 0), (2, 0), "RIGHT"),  # တံဆိပ်တုံးဘောင်ကို ညာဘက်ကပ်မယ်
            ]
        )
    )

    elements.append(header_table)
    elements.append(Spacer(1, 20))  # နေရာလွတ်လေး ချန်မယ်

    # ၃။ ဇယားဒေတာ (Table Data)
    # စာရွက်ထဲကအတိုင်း Header တွေ ရေးမယ်
    data = [
        [
            "利用日",
            "交通機関",
            "利用区間",
            "",
            "",
            "片道|往復",
            "目的・事由",
            "利用金額",
        ],
        # ဒုတိယ header row (ဥပမာ- မှ/သို့)
        ["", "", "から", "~", "まで", "", "", ""],
    ]

    # Database ထဲက data တွေကို ဖြည့်မယ်
    expenses = Expense.objects.filter(date__month=month, date__year=year).order_by(
        "date"
    )

    total = 0
    for item in expenses:
        data.append(
            [
                item.date.strftime("%Y/%m/%d"),
                item.transport,
                item.start_location,
                "~",
                item.end_location,
                item.trip_type,
                item.purpose,
                item.amount,
            ]
        )
        total += item.amount

    # ၄။ စုစုပေါင်း (Total Row)
    data.append(["", "", "", "", "", "", "合計", total])

    # ၅။ ဇယားပုံစံပြင်ခြင်း (Table Styling)
    # စာရွက်ပေါ်ကအတိုင်း မျဉ်းကြောင်းတွေ ဆွဲမယ်
    table = Table(data, colWidths=[70, 60, 80, 20, 80, 50, 100, 60])
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 1), colors.lightgrey),  # Header ကို မီးခိုးရောင်ခြယ်မယ်
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "MSGothic"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),  # မျဉ်းကြောင်းအကုန်ဆွဲမယ်
            ("SPAN", (2, 0), (4, 0)),  # '利用区間' ကို ၃ ကွက်ပေါင်းမယ်
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    )
    table.setStyle(style)
    elements.append(table)

    # ၆။ PDF ထုတ်မယ်
    doc.build(elements)
    buffer.seek(0)

    filename = f"交通費申請書_{year}_{month}.pdf"
    return FileResponse(buffer, as_attachment=True, filename=filename)


def main(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render())
