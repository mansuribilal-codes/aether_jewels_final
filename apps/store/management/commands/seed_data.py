from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile
from apps.store.models import Category, Product, ProductReview
from apps.cart.models import Coupon
from apps.orders.models import Order, OrderItem
from apps.consultations.models import ConsultationBooking
from decimal import Decimal
import datetime


class Command(BaseCommand):
    help = 'Seeds initial luxury jewellery categories, products, coupons, and sample users for Aether Jewels'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(">>> Beginning Aether Jewels luxury database seeding..."))

        # 1. Create Superuser & Demo Users
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'concierge@aetherjewels.com',
                'first_name': 'Sovereign',
                'last_name': 'Admin',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("[OK] Superuser created: admin / admin123"))

        # Demo Client 1 (Aarav Sharma - Mumbai)
        user1, created = User.objects.get_or_create(
            username='aarav_sharma',
            defaults={
                'email': 'aarav.sharma@luxury.in',
                'first_name': 'Aarav',
                'last_name': 'Sharma',
            }
        )
        if created:
            user1.set_password('luxury123')
            user1.save()
            profile1 = user1.profile
            profile1.phone_number = "+91 98201 54321"
            profile1.address_line1 = "Penthouse 18B, Altamount Solitaire Towers"
            profile1.address_line2 = "Altamount Road, Cumballa Hill"
            profile1.landmark = "Near Ambani Residence"
            profile1.city = "Mumbai"
            profile1.state = "Maharashtra"
            profile1.pincode = "400026"
            profile1.vip_tier = "Solitaire Platinum"
            profile1.save()
            self.stdout.write(self.style.SUCCESS("[OK] Demo VIP user created: aarav_sharma / luxury123"))

        # Demo Client 2 (Priya Singhania - Delhi)
        user2, created = User.objects.get_or_create(
            username='priya_singhania',
            defaults={
                'email': 'priya.singhania@heritage.in',
                'first_name': 'Priya',
                'last_name': 'Singhania',
            }
        )
        if created:
            user2.set_password('luxury123')
            user2.save()
            profile2 = user2.profile
            profile2.phone_number = "+91 99100 87654"
            profile2.address_line1 = "Villa 9, Amrita Shergill Marg"
            profile2.address_line2 = "Lutyens Bungalow Zone"
            profile2.landmark = "Near Lodhi Gardens"
            profile2.city = "Delhi"
            profile2.state = "Delhi"
            profile2.pincode = "110003"
            profile2.vip_tier = "Gold Celestial"
            profile2.save()
            self.stdout.write(self.style.SUCCESS("[OK] Demo VIP user created: priya_singhania / luxury123"))

        # 2. Categories
        categories_data = [
            {
                'name': 'Celestial Rings',
                'slug': 'celestial-rings',
                'description': 'Ethereal bands, eternity rings, and halo diamond rings echoing interstellar constellations.',
                'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1000&q=85',
                'order': 1,
            },
            {
                'name': 'Astral Necklaces',
                'slug': 'astral-necklaces',
                'description': 'Statement chokers, floating diamond rivieres, and celestial pendant necklaces crafted in pure gold.',
                'image_url': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1000&q=85',
                'order': 2,
            },
            {
                'name': 'Starlight Earrings',
                'slug': 'starlight-earrings',
                'description': 'Cascading diamond chandeliers, ear jackets, and celestial solitaire studs shimmering with astral light.',
                'image_url': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=1000&q=85',
                'order': 3,
            },
            {
                'name': 'Solar Bracelets',
                'slug': 'solar-bracelets',
                'description': 'Artisanal bangles, diamond tennis bracelets, and cuff talismans radiating solar warmth.',
                'image_url': 'https://images.unsplash.com/photo-1611591475806-9076c8c4be9d?auto=format&fit=crop&w=1000&q=85',
                'order': 4,
            },
            {
                'name': 'High Solitaires',
                'slug': 'high-solitaires',
                'description': 'Certified D-Flawless rare diamonds set in sovereign platinum and celestial 18K yellow gold.',
                'image_url': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=1000&q=85',
                'order': 5,
            },
            {
                'name': 'Zodiac Talismans',
                'slug': 'zodiac-talismans',
                'description': 'Planetary gemstones, astrological birthstone medallions, and sacred celestial amulets.',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1000&q=85',
                'order': 6,
            },
        ]

        cats_map = {}
        for cdata in categories_data:
            cat, _ = Category.objects.update_or_create(
                slug=cdata['slug'],
                defaults=cdata
            )
            cats_map[cdata['slug']] = cat
            self.stdout.write(f"  -> Category: {cat.name}")

        # 3. Sample Products (16 High-end Celestial Luxury Products)
        products_data = [
            # Celestial Rings
            {
                'category': cats_map['celestial-rings'],
                'name': 'The Nebula Empress Diamond Ring',
                'slug': 'nebula-empress-diamond-ring',
                'sku': 'AJ-RNG-01',
                'tagline': 'A cosmic whirlpool of VVS1 diamonds enveloped in 18K Yellow Gold',
                'price': Decimal('185000.00'),
                'original_price': Decimal('210000.00'),
                'stock': 4,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'short_description': 'Featuring an elevated 1.50 carat center diamond surrounded by a micro-pave cosmic halo in handcrafted 18K gold.',
                'description': 'Inspired by the celestial splendor of the Orion Nebula, this masterwork captures incandescent cosmic light. Each diamond is hand-selected by our master gemologists in Mumbai and set under microscopic precision in rich 18K champagne yellow gold.',
                'metal_karat': '18K Yellow Gold',
                'metal_weight_grams': Decimal('6.85'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('1.85'),
                'diamond_clarity': 'VVS1 - IF',
                'diamond_cut': 'Ideal Round Brilliant',
                'certification': '100% BIS Hallmarked & IGI Certified (IGI Diamond Report Included)',
                'dimensions': 'Band Width: 3.2mm | Crown: 11.5mm',
                'size_options': '7, 8, 9, 10, 11, 12, 14',
                'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=1200&q=85',
                'image_url_3': 'https://images.unsplash.com/photo-1598560917505-59a3ad559071?auto=format&fit=crop&w=1200&q=85',
                'image_url_4': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.95'),
                'reviews_count': 24,
            },
            {
                'category': cats_map['celestial-rings'],
                'name': 'Cassiopeia Starlight Rose Gold Band',
                'slug': 'cassiopeia-starlight-rose-gold-band',
                'sku': 'AJ-RNG-02',
                'tagline': 'An eternity constellation band crafted in warm 18K Rose Gold',
                'price': Decimal('98000.00'),
                'original_price': Decimal('115000.00'),
                'stock': 8,
                'is_featured': False,
                'is_bestseller': True,
                'is_new_arrival': True,
                'short_description': 'Interlocking constellation starbursts bezel-set with round brilliant diamonds in 18K rose gold.',
                'description': 'A daily reminder of eternal celestial harmony. The Cassiopeia band features alternating marquise and round diamonds that encircle the finger with effortless comfort and ethereal brilliance.',
                'metal_karat': '18K Rose Gold',
                'metal_weight_grams': Decimal('4.90'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('0.95'),
                'diamond_clarity': 'VS1 - VVS2',
                'diamond_cut': 'Excellent Cut',
                'certification': '100% BIS Hallmarked & SGL Certified',
                'dimensions': 'Band Width: 2.8mm',
                'size_options': '6, 7, 8, 9, 10, 11, 12',
                'image_url': 'https://images.unsplash.com/photo-1603561596112-0a132b757442?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=85',
                'image_url_3': 'https://images.unsplash.com/photo-1598560917505-59a3ad559071?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.88'),
                'reviews_count': 16,
            },
            {
                'category': cats_map['celestial-rings'],
                'name': 'Zambian Royal Solstice Emerald Ring',
                'slug': 'zambian-royal-solstice-emerald-ring',
                'sku': 'AJ-RNG-03',
                'tagline': 'An intensely saturated 3.20 ct Royal Zambian Emerald flanked by trapezoid diamonds',
                'price': Decimal('425000.00'),
                'original_price': Decimal('480000.00'),
                'stock': 2,
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': True,
                'short_description': 'A collector-grade vivid green emerald set in 18K yellow gold with celestial diamond shoulders.',
                'description': 'Unrivaled verdant majesty. Sourced directly from premier Zambian mines, this octagonal step-cut emerald exhibits mesmerizing depth, framed by stepped diamond baguette facets for sovereign grandeur.',
                'metal_karat': '18K Yellow Gold',
                'metal_weight_grams': Decimal('8.40'),
                'gemstone_type': 'Zambian Emerald',
                'diamond_carat': Decimal('1.10'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Step Cut & Trapezoid',
                'certification': '100% BIS Hallmarked & GRS Gemstone Certification',
                'dimensions': 'Emerald: 9.8mm x 7.9mm',
                'size_options': '8, 9, 10, 12, 14, 16',
                'image_url': 'https://images.unsplash.com/photo-1598560917505-59a3ad559071?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=85',
                'image_url_3': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('5.00'),
                'reviews_count': 9,
            },

            # Astral Necklaces
            {
                'category': cats_map['astral-necklaces'],
                'name': 'The Sovereign Galaxy Diamond Riviere',
                'slug': 'sovereign-galaxy-diamond-riviere',
                'sku': 'AJ-NCK-01',
                'tagline': 'A continuous stream of 12.5 carats of graduating celestial diamonds',
                'price': Decimal('1280000.00'),
                'original_price': Decimal('1450000.00'),
                'stock': 2,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'short_description': 'Graduating round brilliant diamonds hand-strung in 18K white gold with sovereign safety clasp.',
                'description': 'The pinnacle of high jewellery craftsmanship. Each of the 108 diamonds is individually calibrated for color and luminescence, creating an unbroken river of liquid fire around the collarbone.',
                'metal_karat': '18K White Gold',
                'metal_weight_grams': Decimal('32.40'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('12.50'),
                'diamond_clarity': 'VVS1 - IF',
                'diamond_cut': 'Ideal Hearts & Arrows Brilliant',
                'certification': '100% BIS Hallmarked & IGI High Jewellery Dossier',
                'dimensions': 'Length: 16.5 inches (Adjustable to 17.5 in)',
                'size_options': '16.5 inches, 18.0 inches',
                'image_url': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1200&q=85',
                'image_url_3': 'https://images.unsplash.com/photo-1611591475806-9076c8c4be9d?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('5.00'),
                'reviews_count': 14,
            },
            {
                'category': cats_map['astral-necklaces'],
                'name': 'Astraea Solar Pendant Necklace',
                'slug': 'astraea-solar-pendant-necklace',
                'sku': 'AJ-NCK-02',
                'tagline': 'Sunburst medallions crowned with a golden yellow diamond center',
                'price': Decimal('145000.00'),
                'original_price': Decimal('165000.00'),
                'stock': 6,
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': True,
                'short_description': 'Radial sun rays of pave diamonds encircling a central cushion-cut canary yellow diamond.',
                'description': 'Inspired by Astraea, goddess of celestial light and purity. Suspended from an intricate Italian wheat chain in 18K dual gold.',
                'metal_karat': 'Dual Tone 18K Gold',
                'metal_weight_grams': Decimal('7.80'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('1.45'),
                'diamond_clarity': 'VVS2',
                'diamond_cut': 'Cushion Brilliant',
                'certification': '100% BIS Hallmarked & SGL Certified',
                'dimensions': 'Pendant: 22mm Diameter | Chain: 18 in',
                'size_options': '16-18 in Adjustable',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.92'),
                'reviews_count': 19,
            },
            {
                'category': cats_map['astral-necklaces'],
                'name': 'Ceylon Midnight Sapphire Astral Collar',
                'slug': 'ceylon-midnight-sapphire-astral-collar',
                'sku': 'AJ-NCK-03',
                'tagline': 'Royal velvet blue Ceylon Sapphires interspersed with starlight diamonds',
                'price': Decimal('680000.00'),
                'original_price': Decimal('750000.00'),
                'stock': 3,
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': False,
                'short_description': '7 unheated Royal Blue Ceylon sapphires weighing 8.2 carats in 18K white gold.',
                'description': 'Reflecting the indigo depths of the midnight galaxy. Unheated natural blue sapphires with exceptional crystal clarity, handcrafted for high-society gala occasions and royal weddings.',
                'metal_karat': '18K White Gold',
                'metal_weight_grams': Decimal('22.10'),
                'gemstone_type': 'Ceylon Sapphire',
                'diamond_carat': Decimal('3.80'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Oval & Pear Cut',
                'certification': '100% BIS Hallmarked & SSEF / GRS Certified',
                'dimensions': 'Collar Length: 16 inches',
                'size_options': '16.0 inches Standard',
                'image_url': 'https://images.unsplash.com/photo-1611591475806-9076c8c4be9d?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.96'),
                'reviews_count': 11,
            },

            # Starlight Earrings
            {
                'category': cats_map['starlight-earrings'],
                'name': 'Pleiades Cascade Diamond Chandeliers',
                'slug': 'pleiades-cascade-diamond-chandeliers',
                'sku': 'AJ-EAR-01',
                'tagline': 'A cascading dance of pear and marquise cut diamonds inspired by the Seven Sisters',
                'price': Decimal('340000.00'),
                'original_price': Decimal('390000.00'),
                'stock': 4,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'short_description': 'Articulated drops that sway with graceful movement, catching ambient light from every angle.',
                'description': 'The Pleiades chandelier earrings feature 4.2 carats of graded natural diamonds in feather-light 18K white gold settings, engineered for all-night comfort without weight compromise.',
                'metal_karat': '18K White Gold',
                'metal_weight_grams': Decimal('11.20'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('4.20'),
                'diamond_clarity': 'VVS2 - VS1',
                'diamond_cut': 'Pear & Marquise Brilliant',
                'certification': '100% BIS Hallmarked & IGI Certified',
                'dimensions': 'Length: 48mm | Width: 18mm',
                'size_options': 'Standard Drop',
                'image_url': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.94'),
                'reviews_count': 22,
            },
            {
                'category': cats_map['starlight-earrings'],
                'name': 'Andromeda Solitaire Halo Studs',
                'slug': 'andromeda-solitaire-halo-studs',
                'sku': 'AJ-EAR-02',
                'tagline': 'Twin 1.00 ct D-Color certified diamond solitaires wrapped in micro-pave halos',
                'price': Decimal('225000.00'),
                'original_price': Decimal('250000.00'),
                'stock': 7,
                'is_featured': False,
                'is_bestseller': True,
                'is_new_arrival': True,
                'short_description': 'Timeless everyday grandeur with screw-back luxury security posts in 18K Yellow Gold.',
                'description': 'Effortless luxury. Featuring matched pair D/IF diamonds that exude hypnotic scintillation, enclosed in our signature starry halo gallery.',
                'metal_karat': '18K Yellow Gold',
                'metal_weight_grams': Decimal('4.10'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('2.30'),
                'diamond_clarity': 'VVS1 - IF',
                'diamond_cut': 'Ideal Round Brilliant',
                'certification': '100% BIS Hallmarked & IGI Dual Dossier',
                'dimensions': 'Diameter: 8.5mm',
                'size_options': 'Screw Back, Push Back',
                'image_url': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.98'),
                'reviews_count': 31,
            },
            {
                'category': cats_map['starlight-earrings'],
                'name': 'Burmese Royal Ruby Starlight Drops',
                'slug': 'burmese-royal-ruby-starlight-drops',
                'sku': 'AJ-EAR-03',
                'tagline': 'Natural unheated Pigeon Blood Rubies framed in celestial gold lace',
                'price': Decimal('475000.00'),
                'original_price': Decimal('520000.00'),
                'stock': 3,
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': True,
                'short_description': 'Rare Burmese natural rubies weighing 3.80 carats in royal 22K yellow gold settings.',
                'description': 'Fiery passion meets royal heritage. Handcrafted in Rajasthan and finished in Mumbai with old-world Kundan setting refinement merged with modern high-precision prongs.',
                'metal_karat': '22K Royal Gold',
                'metal_weight_grams': Decimal('9.60'),
                'gemstone_type': 'Burmese Ruby',
                'diamond_carat': Decimal('1.60'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Cushion Cut Rubies & Brilliant Diamonds',
                'certification': '100% BIS Hallmarked & Gubelin Ruby Report',
                'dimensions': 'Length: 35mm',
                'size_options': 'Standard Drop',
                'image_url': 'https://images.unsplash.com/photo-1598560917505-59a3ad559071?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1630019852942-f89202989a59?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('5.00'),
                'reviews_count': 8,
            },

            # Solar Bracelets
            {
                'category': cats_map['solar-bracelets'],
                'name': 'The Helios Celestial Diamond Tennis Bracelet',
                'slug': 'helios-celestial-diamond-tennis-bracelet',
                'sku': 'AJ-BRC-01',
                'tagline': '6.00 carats of precision four-prong diamonds in flexible 18K Yellow Gold',
                'price': Decimal('490000.00'),
                'original_price': Decimal('550000.00'),
                'stock': 5,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'short_description': 'Fluid articulation and double safety clasp for lifetime durability and sovereign poise.',
                'description': 'The quintessential mark of discerning luxury. Crafted with seamless links that drape like silk against the wrist, each diamond calibrated to absolute perfection.',
                'metal_karat': '18K Yellow Gold',
                'metal_weight_grams': Decimal('14.80'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('6.00'),
                'diamond_clarity': 'VVS2 - VS1',
                'diamond_cut': 'Ideal Round Brilliant',
                'certification': '100% BIS Hallmarked & IGI Certified',
                'dimensions': 'Length: 7.0 inches (Custom sizing available)',
                'size_options': '6.5 in, 7.0 in, 7.5 in',
                'image_url': 'https://images.unsplash.com/photo-1611591475806-9076c8c4be9d?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.97'),
                'reviews_count': 28,
            },
            {
                'category': cats_map['solar-bracelets'],
                'name': 'Solstice Astral Open Cuff Bangle',
                'slug': 'solstice-astral-open-cuff-bangle',
                'sku': 'AJ-BRC-02',
                'tagline': 'Rigid sculpted 18K Rose Gold cuff tipped with pear-shaped solitaire terminals',
                'price': Decimal('210000.00'),
                'original_price': Decimal('240000.00'),
                'stock': 6,
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': True,
                'short_description': 'A contemporary architectural silhouette featuring 1.75 carats of pave and pear diamonds.',
                'description': 'Bold yet refined. The Solstice Cuff hugs the wrist with engineered spring-tension memory, rendering clasps unnecessary while offering flawless security.',
                'metal_karat': '18K Rose Gold',
                'metal_weight_grams': Decimal('16.50'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('1.75'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Pear & Pave Brilliant',
                'certification': '100% BIS Hallmarked & SGL Certified',
                'dimensions': 'Inner Diameter: 58mm',
                'size_options': 'Small (2.2), Medium (2.4), Large (2.6)',
                'image_url': 'https://images.unsplash.com/photo-1603561596112-0a132b757442?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1611591475806-9076c8c4be9d?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.89'),
                'reviews_count': 15,
            },

            # High Solitaires
            {
                'category': cats_map['high-solitaires'],
                'name': 'The Polaris 3.00 Carat D-Flawless Solitaire',
                'slug': 'polaris-3ct-d-flawless-solitaire',
                'sku': 'AJ-SOL-01',
                'tagline': 'A pinnacle 3.00 Carat Type IIa Diamond in handcrafted 950 Pure Platinum',
                'price': Decimal('950000.00'),
                'original_price': Decimal('1100000.00'),
                'stock': 1,
                'is_featured': True,
                'is_bestseller': True,
                'is_new_arrival': False,
                'short_description': 'The crown jewel of our celestial atelier. GIA Triple Excellent, completely colorless D/IF purity.',
                'description': 'Representing less than 0.01% of all gem-grade diamonds on Earth. Set in our proprietary six-prong Lotus Crown in 950 platinum with hidden diamond under-gallery accents.',
                'metal_karat': '950 Pure Platinum',
                'metal_weight_grams': Decimal('7.20'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('3.00'),
                'diamond_clarity': 'Flawless',
                'diamond_cut': 'GIA Triple Excellent 3EX',
                'certification': '100% BIS Hallmarked & GIA Diamond Dossier + Laser Inscription',
                'dimensions': 'Diamond: 9.35mm x 9.39mm x 5.78mm',
                'size_options': '7, 8, 9, 10, 11, 12, 14, 16',
                'image_url': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=85',
                'image_url_3': 'https://images.unsplash.com/photo-1598560917505-59a3ad559071?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('5.00'),
                'reviews_count': 19,
            },
            {
                'category': cats_map['high-solitaires'],
                'name': 'Aether Oval Celestial Solitaire Ring',
                'slug': 'aether-oval-celestial-solitaire-ring',
                'sku': 'AJ-SOL-02',
                'tagline': 'An elongated 2.20 carat Oval Cut diamond with cathedral diamond band',
                'price': Decimal('580000.00'),
                'original_price': Decimal('640000.00'),
                'stock': 3,
                'is_featured': True,
                'is_bestseller': False,
                'is_new_arrival': True,
                'short_description': 'Flattering elongated proportions with zero bow-tie effect in 18K yellow gold.',
                'description': 'Masterfully faceted to maximize brilliance and fire. The slender 1.8mm micropave band creates the illusion that the diamond floats effortlessly above the skin.',
                'metal_karat': '18K Yellow Gold',
                'metal_weight_grams': Decimal('5.10'),
                'gemstone_type': 'Natural Diamond',
                'diamond_carat': Decimal('2.65'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Oval Celestial Cut',
                'certification': '100% BIS Hallmarked & IGI Certified',
                'dimensions': 'Center Gem: 10.4mm x 7.2mm',
                'size_options': '6, 7, 8, 9, 10, 11, 12, 14',
                'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.95'),
                'reviews_count': 17,
            },

            # Zodiac Talismans
            {
                'category': cats_map['zodiac-talismans'],
                'name': 'The Sovereign Sun God Surya Talisman',
                'slug': 'sovereign-sun-god-surya-talisman',
                'sku': 'AJ-TAL-01',
                'tagline': 'Natural Burmese Ruby & Navratna planetary gemstones in sacred 22K Royal Gold',
                'price': Decimal('165000.00'),
                'original_price': Decimal('185000.00'),
                'stock': 5,
                'is_featured': False,
                'is_bestseller': True,
                'is_new_arrival': True,
                'short_description': 'Astrologically potent planetary amulet hand-engraved with celestial Sanskrit glyphs.',
                'description': 'Harmonizing cosmic planetary energies with haute joaillerie finesse. Featuring 9 flawless astrological gemstones set according to Vedic principles in hallmarked 22K gold.',
                'metal_karat': '22K Royal Gold',
                'metal_weight_grams': Decimal('12.40'),
                'gemstone_type': 'Burmese Ruby',
                'diamond_carat': Decimal('0.85'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Cabochon & Brilliant Cut',
                'certification': '100% BIS Hallmarked & Gemological Vedic Certificate',
                'dimensions': 'Diameter: 28mm',
                'size_options': 'Pendant with 20 in Gold Chain',
                'image_url': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.96'),
                'reviews_count': 20,
            },
            {
                'category': cats_map['zodiac-talismans'],
                'name': 'Tanzanite Starlight Astral Signet',
                'slug': 'tanzanite-starlight-astral-signet',
                'sku': 'AJ-TAL-02',
                'tagline': 'Deep indigo-violet 4.50 ct AAA Tanzanite in heavy brushed 18K Gold',
                'price': Decimal('275000.00'),
                'original_price': Decimal('310000.00'),
                'stock': 3,
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': True,
                'short_description': 'Heirloom signet ring with engraved star charts and pave diamond starburst shoulders.',
                'description': 'Sourced from the foothills of Mount Kilimanjaro, this rare pleochroic tanzanite flashes shades of celestial purple and deep sapphire blue, enclosed in a substantial brushed gold signet.',
                'metal_karat': '18K Yellow Gold',
                'metal_weight_grams': Decimal('14.20'),
                'gemstone_type': 'Tanzanite & Diamond',
                'diamond_carat': Decimal('0.75'),
                'diamond_clarity': 'VVS2',
                'diamond_cut': 'Cushion Cut Tanzanite',
                'certification': '100% BIS Hallmarked & SGL Certified',
                'dimensions': 'Top Face: 16mm x 14mm',
                'size_options': '10, 12, 14, 16, 18, 20',
                'image_url': 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1603561591411-07134e71a2a9?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.91'),
                'reviews_count': 12,
            },
            {
                'category': cats_map['zodiac-talismans'],
                'name': 'Luna South Sea Pearl Celestial Brooch',
                'slug': 'luna-south-sea-pearl-celestial-brooch',
                'sku': 'AJ-TAL-03',
                'tagline': '13.5mm Lustrous Golden South Sea Pearl wrapped in a diamond crescent moon',
                'price': Decimal('195000.00'),
                'original_price': Decimal('220000.00'),
                'stock': 4,
                'is_featured': False,
                'is_bestseller': False,
                'is_new_arrival': False,
                'short_description': 'An opulent crescent brooch and pendant convertible in 18K yellow and white gold.',
                'description': 'Harnessing the serene gravitational power of the Moon. A flawless, naturally golden South Sea pearl cradled within a diamond crescent moon, wearable both as a brooch and statement pendant.',
                'metal_karat': 'Dual Tone 18K Gold',
                'metal_weight_grams': Decimal('11.50'),
                'gemstone_type': 'South Sea Pearl',
                'diamond_carat': Decimal('1.20'),
                'diamond_clarity': 'VVS1',
                'diamond_cut': 'Ideal Brilliant',
                'certification': '100% BIS Hallmarked & Pearl Origin Certificate',
                'dimensions': 'Brooch: 38mm x 32mm',
                'size_options': 'Convertible Brooch/Pendant',
                'image_url': 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?auto=format&fit=crop&w=1200&q=85',
                'image_url_2': 'https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?auto=format&fit=crop&w=1200&q=85',
                'rating': Decimal('4.88'),
                'reviews_count': 15,
            },
        ]

        for pdata in products_data:
            p, created = Product.objects.update_or_create(
                slug=pdata['slug'],
                defaults=pdata
            )
            self.stdout.write(f"  [OK] Product: {p.name} [{p.sku}] - Rs. {p.price}")

            # Sample review for product
            if created:
                ProductReview.objects.create(
                    product=p,
                    user=user1,
                    rating=5,
                    title="Exquisite Craftsmanship & Unmatched Sparkle",
                    comment=f"Received the {p.name} in Mumbai with armored courier service. The IGI certificate and the gold lustre in person is breathtaking. True sovereign luxury.",
                    verified_purchase=True
                )

        # 4. Create Promotional Coupons
        coupons_data = [
            {
                'code': 'AETHERLIV',
                'description': '10% Celestial Welcome Privilege on orders above Rs. 50,000',
                'discount_percent': 10,
                'discount_amount': Decimal('0.00'),
                'min_purchase': Decimal('50000.00'),
                'is_active': True,
            },
            {
                'code': 'CELESTIAL',
                'description': 'Flat Rs. 10,000 Sovereign Privilege on orders above Rs. 1,00,000',
                'discount_percent': 0,
                'discount_amount': Decimal('10000.00'),
                'min_purchase': Decimal('100000.00'),
                'is_active': True,
            },
            {
                'code': 'ROYALTY15',
                'description': '15% Solitaire Platinum Club Privilege on orders above Rs. 2,00,000',
                'discount_percent': 15,
                'discount_amount': Decimal('0.00'),
                'min_purchase': Decimal('200000.00'),
                'is_active': True,
            },
        ]

        for cdata in coupons_data:
            c, _ = Coupon.objects.update_or_create(
                code=cdata['code'],
                defaults=cdata
            )
            self.stdout.write(f"  [Coupon] {c.code} ({c.description})")

        # 5. Sample Past Order for user1
        sample_prod = Product.objects.get(sku='AJ-RNG-01')
        order, o_created = Order.objects.get_or_create(
            order_number='AJ-2026-88194',
            defaults={
                'user': user1,
                'full_name': 'Aarav Sharma',
                'email': user1.email,
                'phone': '+91 98201 54321',
                'address_line1': 'Penthouse 18B, Altamount Solitaire Towers',
                'address_line2': 'Altamount Road, Cumballa Hill',
                'landmark': 'Near Ambani Residence',
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400026',
                'payment_method': 'UPI',
                'payment_status': 'Paid',
                'order_status': 'Dispatched',
                'subtotal': sample_prod.price,
                'discount': Decimal('18500.00'),
                'tax_gst': Decimal('4995.00'),
                'grand_total': Decimal('171495.00'),
                'coupon_code': 'AETHERLIV',
                'tracking_number': 'BLUEDART-SECURE-992817',
                'gift_message': 'Happy 10th Anniversary to my celestial queen.',
            }
        )
        if o_created:
            OrderItem.objects.create(
                order=order,
                product=sample_prod,
                product_name=sample_prod.name,
                product_sku=sample_prod.sku,
                product_image_url=sample_prod.image_url,
                selected_size='9',
                price=sample_prod.price,
                quantity=1
            )
            self.stdout.write(self.style.SUCCESS("[OK] Sample luxury order created for Aarav Sharma"))

        # 6. Sample Consultation Booking
        ConsultationBooking.objects.get_or_create(
            name='Priya Singhania',
            email='priya.singhania@heritage.in',
            defaults={
                'phone': '+91 99100 87654',
                'consultation_type': 'Delhi Boutique',
                'preferred_date': datetime.date.today() + datetime.timedelta(days=3),
                'time_slot': '04:30 PM - 06:30 PM',
                'interest_category': 'Bridal',
                'budget_range': 'Rs. 15,00,000+ Sovereign',
                'notes': 'Interested in bespoke bridal diamond choker necklace and matching earrings for winter wedding in Udaipur.',
                'status': 'Confirmed'
            }
        )

        self.stdout.write(self.style.SUCCESS("\n>>> Aether Jewels Luxury Database successfully seeded!"))
        self.stdout.write(self.style.NOTICE("Admin credentials: admin / admin123"))
        self.stdout.write(self.style.NOTICE("Demo VIP client: aarav_sharma / luxury123"))
