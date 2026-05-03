from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
from django.template.loader import render_to_string
from .models import Payment, Invoice
from .forms import PaymentForm
from members.views import get_branch_filter


@login_required
def payment_list(request):
    branch_filter = get_branch_filter(request.user)
    payments = Payment.objects.filter(member__branch__in=request.user.get_accessible_branches())
    return render(request, 'payments/list.html', {'payments': payments})


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            payment = form.save()
            invoice = Invoice.objects.create(payment=payment)
            messages.success(request, f'Payment recorded. Invoice #{invoice.invoice_number} generated.')
            return redirect('payments:detail', pk=payment.pk)
    else:
        member_id = request.GET.get('member')
        form = PaymentForm(user=request.user, initial={'member': member_id} if member_id else {})
    return render(request, 'payments/form.html', {'form': form, 'title': 'Record Payment'})


@login_required
def payment_detail(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    return render(request, 'payments/detail.html', {'payment': payment})


@login_required
def pending_payments(request):
    branches = request.user.get_accessible_branches()
    today = timezone.now().date()
    pending = Payment.objects.filter(
        member__branch__in=branches,
        status__in=['pending', 'overdue']
    )
    return render(request, 'payments/pending.html', {'payments': pending})


@login_required
def invoice_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    import io

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
        rightMargin=20*mm, leftMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm)

    PURPLE = colors.HexColor('#7F77DD')
    DARK   = colors.HexColor('#1A1A2E')
    GRAY   = colors.HexColor('#666666')
    LIGHT  = colors.HexColor('#F8F9FB')

    title_style  = ParagraphStyle('title', fontSize=28, textColor=PURPLE, fontName='Helvetica-Bold', spaceAfter=4)
    sub_style    = ParagraphStyle('sub',   fontSize=11, textColor=GRAY,   fontName='Helvetica', spaceAfter=2)
    normal_style = ParagraphStyle('norm',  fontSize=11, textColor=DARK,   fontName='Helvetica', spaceAfter=4)
    label_style  = ParagraphStyle('lbl',   fontSize=9,  textColor=GRAY,   fontName='Helvetica', spaceAfter=2)

    p      = invoice.payment
    member = p.member
    elements = []

    # Header row
    header_data = [[
        Paragraph('GymFlow', title_style),
        Paragraph(
            f'INVOICE<br/><font size="10" color="#666666">#{invoice.invoice_number}</font>',
            ParagraphStyle('inv', fontSize=22, fontName='Helvetica-Bold',
                           textColor=DARK, alignment=TA_RIGHT)
        ),
    ]]
    header_table = Table(header_data, colWidths=[90*mm, 80*mm])
    header_table.setStyle(TableStyle([
        ('VALIGN',      (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW',   (0,0), (-1, 0), 1, PURPLE),
        ('BOTTOMPADDING',(0,0),(-1, 0), 10),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8*mm))
    elements.append(Paragraph(member.branch.name, sub_style))
    elements.append(Spacer(1, 6*mm))

    # Billed to + invoice date
    info_data = [[
        [Paragraph('BILLED TO', label_style),
         Paragraph(f'<b>{member.full_name}</b>', normal_style),
         Paragraph(member.phone, normal_style),
         Paragraph(member.email or '', normal_style),
         Paragraph(f'Member ID: {member.member_id}',
                   ParagraphStyle('mid', fontSize=9, textColor=GRAY, fontName='Helvetica'))],
        [Paragraph('INVOICE DATE', label_style),
         Paragraph(str(invoice.issued_on), normal_style),
         Paragraph('RECEIPT NO.', label_style),
         Paragraph(f'<b>{p.receipt_number}</b>', normal_style),
         Paragraph('STATUS', label_style),
         Paragraph(f'<b>{p.get_status_display()}</b>', normal_style)],
    ]]
    info_table = Table(info_data, colWidths=[95*mm, 75*mm])
    info_table.setStyle(TableStyle([
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('BACKGROUND', (0,0), (-1,-1), LIGHT),
        ('PADDING',    (0,0), (-1,-1), 8),
    ]))
    elements.append(info_table)
    elements.append(Spacer(1, 8*mm))

    # Line items
    item_data = [
        ['Description', 'Period', 'Amount', 'Discount', 'Total'],
        [
            p.plan.name if p.plan else 'Membership',
            f'{p.coverage_from} to {p.coverage_to}',
            f'Rs.{p.amount}',
            f'Rs.{p.discount}',
            f'Rs.{p.final_amount}',
        ],
        ['', '', '', 'Total Paid', f'Rs.{p.final_amount}'],
    ]
    item_table = Table(item_data, colWidths=[55*mm, 50*mm, 22*mm, 22*mm, 21*mm])
    item_table.setStyle(TableStyle([
        ('BACKGROUND',   (0,0), (-1, 0), PURPLE),
        ('TEXTCOLOR',    (0,0), (-1, 0), colors.white),
        ('FONTNAME',     (0,0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0), (-1,-1), 10),
        ('FONTNAME',     (0,-1),(-1,-1), 'Helvetica-Bold'),
        ('LINEABOVE',    (0,-1),(-1,-1), 1, PURPLE),
        ('GRID',         (0,0), (-1,-2), 0.3, colors.HexColor('#DDDDDD')),
        ('PADDING',      (0,0), (-1,-1), 7),
        ('ALIGN',        (2,0), (-1,-1), 'RIGHT'),
        ('ROWBACKGROUNDS',(0,1),(-1,-2), [colors.white, LIGHT]),
    ]))
    elements.append(item_table)
    elements.append(Spacer(1, 6*mm))

    # Payment method line
    meta = f'Payment method: {p.get_method_display()}'
    if p.paid_on:
        meta += f'     Paid on: {p.paid_on}'
    elements.append(Paragraph(meta,
        ParagraphStyle('meta', fontSize=9, textColor=GRAY, fontName='Helvetica')))
    elements.append(Spacer(1, 16*mm))

    # Footer
    elements.append(Paragraph(
        f'Thank you for being a valued member of {member.branch.name}!',
        ParagraphStyle('footer', fontSize=10, textColor=GRAY,
                       fontName='Helvetica', alignment=TA_CENTER)))
    elements.append(Paragraph('Generated by GymFlow',
        ParagraphStyle('gf', fontSize=9, textColor=colors.HexColor('#AAAAAA'),
                       fontName='Helvetica', alignment=TA_CENTER)))

    doc.build(elements)
    buffer.seek(0)

    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'filename="invoice-{invoice.invoice_number}.pdf"'
    return response
