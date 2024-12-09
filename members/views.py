from django.shortcuts import render, get_object_or_404, redirect
from .forms import MemberCreateForm
from .models import Member
from savings.models import SavingAccount, SavingDeposit, SavingWithdrawal
from loans.models import LoanAccount, LoanIssue, LoanPayment
from shares.models import ShareAccount, ShareSell, ShareBuy


# Create your views here.

def member_create(request):
    template = 'members/form.html'
    form = MemberCreateForm(request.POST or None)

    if form.is_valid():
        member = form.save()  # Save the member instance
        return redirect('members:member_detail', mem_number=member.mem_number)  # Redirect to the detail view

    context = {
        'form': form,
        'title': "Create Member",
    }

    return render(request, template, context)


def member(request):
    template = 'members/members.html'
    members = Member.objects.order_by("mem_number")

    context = {
        'members': members,
    }

    return render(request, template, context)


def member_detail(request, mem_number):
    template = 'members/member_details.html'
    member = get_object_or_404(Member, mem_number=mem_number)

    # Using .filter() to avoid 404 if related accounts do not exist
    saving_ac = SavingAccount.objects.filter(owner=member).first()
    deposit_transactions = SavingDeposit.objects.filter(account=saving_ac, delete_status=False) if saving_ac else []
    withdrawal_transactions = SavingWithdrawal.objects.filter(account=saving_ac,
                                                              delete_status=False) if saving_ac else []

    loan_ac = LoanAccount.objects.filter(owner=member).first()
    pending_loan = LoanIssue.objects.filter(account=loan_ac, status="Pending", delete_status=False) if loan_ac else []
    approved_loan = LoanIssue.objects.filter(account=loan_ac, status="Approved", delete_status=False) if loan_ac else []
    issue_transactions = LoanIssue.objects.filter(account=loan_ac, delete_status=False) if loan_ac else []
    payment_transactions = LoanPayment.objects.filter(loan_num__account=loan_ac, delete_status=False) if loan_ac else []

    share_ac = ShareAccount.objects.filter(owner=member).first()
    sell_transactions = ShareSell.objects.filter(account=share_ac, delete_status=False) if share_ac else []
    buy_transactions = ShareBuy.objects.filter(account=share_ac, delete_status=False) if share_ac else []

    context = {
        'member': member,
        'saving_ac': saving_ac,
        'loan_ac': loan_ac,
        'share_ac': share_ac,
        'pending_loan': pending_loan,
        'approved_loan': approved_loan,
        'deposit_transactions': deposit_transactions,
        'withdrawal_transactions': withdrawal_transactions,
        'issue_transactions': issue_transactions,
        'payment_transactions': payment_transactions,
        'sell_transactions': sell_transactions,
        'buy_transactions': buy_transactions,
    }

    return render(request, template, context)