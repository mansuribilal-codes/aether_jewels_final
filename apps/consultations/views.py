import json
import uuid
import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.consultations.forms import ConsultationBookingForm, BespokeInquiryForm
from apps.consultations.models import ConsultationBooking, BespokeInquiry


def book_consultation_view(request):
    if request.method == 'POST':
        form = ConsultationBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            messages.success(request, f"✨ Your VIP Private Consultation has been scheduled for {booking.preferred_date}. Our Sovereign Concierge will contact you within 2 hours.")
            return redirect('consultations:success', booking_type='appointment', item_id=booking.id)
        else:
            messages.error(request, "Please ensure all appointment details and phone numbers are correctly provided.")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial['email'] = request.user.email
            if hasattr(request.user, 'profile'):
                initial['phone'] = request.user.profile.phone_number
        form = ConsultationBookingForm(initial=initial)

    return render(request, 'consultations/book.html', {
        'form': form,
        'title': 'Book Private VIP Consultation | Aether Jewels',
    })


def bespoke_inquiry_view(request):
    if request.method == 'POST':
        form = BespokeInquiryForm(request.POST)
        if form.is_valid():
            bespoke = form.save()
            messages.success(request, f"✨ Your bespoke commission inquiry for '{bespoke.gemstone_preference}' has been received. Our Master Artisan will prepare an initial rendering.")
            return redirect('consultations:success', booking_type='bespoke', item_id=bespoke.id)
        else:
            messages.error(request, "Please review the bespoke commission form fields.")
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['name'] = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            initial['email'] = request.user.email
            if hasattr(request.user, 'profile'):
                initial['phone'] = request.user.profile.phone_number
                initial['city'] = request.user.profile.city
        form = BespokeInquiryForm(initial=initial)

    return render(request, 'consultations/bespoke.html', {
        'form': form,
        'title': 'Bespoke Haute Joaillerie Atelier | Aether Jewels',
    })


def consultation_success_view(request, booking_type, item_id):
    booking = None
    if booking_type == 'appointment':
        booking = ConsultationBooking.objects.filter(id=item_id).first()
    elif booking_type == 'bespoke':
        booking = BespokeInquiry.objects.filter(id=item_id).first()

    return render(request, 'consultations/success.html', {
        'booking': booking,
        'booking_type': booking_type,
        'title': 'Appointment Confirmed | Aether Jewels Concierge',
    })


def api_book_consultation(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    full_name = data.get('full_name') or data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    city_lounge = data.get('city_lounge') or data.get('consultation_type', 'Mumbai Flagship')
    preferred_date_str = data.get('preferred_date')
    preferred_time = data.get('preferred_time') or data.get('time_slot', '02:00 PM - 04:00 PM')
    jewellery_interest = data.get('jewellery_interest') or data.get('interest_category', 'Solitaires')
    hospitality = data.get('hospitality_preference', '')
    notes = data.get('notes', '').strip()

    if hospitality:
        notes = f"Hospitality: {hospitality} | " + notes

    if not full_name or not email or not phone:
        return JsonResponse({'success': False, 'error': 'Please provide full name, email, and phone contact.'}, status=400)

    try:
        if preferred_date_str:
            preferred_date = datetime.datetime.strptime(preferred_date_str, '%Y-%m-%d').date()
        else:
            preferred_date = datetime.date.today() + datetime.timedelta(days=2)
    except Exception:
        preferred_date = datetime.date.today() + datetime.timedelta(days=2)

    booking = ConsultationBooking.objects.create(
        name=full_name,
        email=email,
        phone=phone,
        consultation_type=city_lounge,
        preferred_date=preferred_date,
        time_slot=preferred_time,
        interest_category=jewellery_interest,
        notes=notes,
        status='Confirmed'
    )

    booking_id = f"AJ-VIP-{booking.id:04d}-{uuid.uuid4().hex[:4].upper()}"

    return JsonResponse({
        'success': True,
        'booking_id': booking_id,
        'message': f'✨ Sovereign Viewing secured for {booking.preferred_date}. Reference: {booking_id}',
    })


def api_bespoke_inquiry(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        data = request.POST

    client_name = data.get('client_name') or data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    piece_type = data.get('piece_type', 'Solitaire Ring')
    gemstone = data.get('gemstone', 'Golconda Flawless Diamond')
    metal = data.get('metal', '18k Celestial Champagne Gold')
    carat_weight = data.get('carat_weight', 4.5)
    setting_style = data.get('setting_style', 'Astral Halo')
    estimated_price_inr = data.get('estimated_price_inr', 0)
    custom_engraving = data.get('custom_engraving', '')
    notes = data.get('notes', '')

    if not client_name or not email or not phone:
        return JsonResponse({'success': False, 'error': 'Please provide client name, email, and phone contact.'}, status=400)

    inquiry = BespokeInquiry.objects.create(
        name=client_name,
        email=email,
        phone=phone,
        piece_type=piece_type,
        gemstone_preference=gemstone,
        metal_preference=metal,
        carat_weight=carat_weight,
        setting_style=setting_style,
        estimated_price_inr=estimated_price_inr,
        custom_engraving=custom_engraving,
        design_idea=notes or f"Commission configuration: {carat_weight}ct {gemstone} set in {metal} ({setting_style}). Engraving: {custom_engraving}",
    )

    inquiry_id = f"AJ-BESPOKE-{inquiry.id:04d}"

    return JsonResponse({
        'success': True,
        'inquiry_id': inquiry_id,
        'message': f'✨ Bespoke Dossier #{inquiry_id} received. Master Jeweller will contact you within 2 hours.',
    })

