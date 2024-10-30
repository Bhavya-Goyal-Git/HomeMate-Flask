from homemate import app,db
from homemate.models.tables import ServiceCategory, User, Service
print("\n\n----------- Welcome to initial Database setup! ------------\n")

with app.app_context():
    try:
        db.drop_all()
    except:
        print("No Previously SetUp Database Found!\n")

    print("----------------- Creating Database ----------------------------\n")
    db.create_all()
    print("----------------- Database Created! ----------------------------\n")
    
    db.session.add(User(username="admin",email_address="admin@admin.com",role="admin",password="admin"))
    
    db.session.add_all([ServiceCategory(title="catering"),
    ServiceCategory(title="cleaning"),
    ServiceCategory(title="electric repairing"),
    ServiceCategory(title="electronic servicing"),
    ServiceCategory(title="event management"),
    ServiceCategory(title="flooring"),
    ServiceCategory(title="gardening"),
    ServiceCategory(title="home beauty"),
    ServiceCategory(title="masonary"),
    ServiceCategory(title="metal fabrications"),
    ServiceCategory(title="nursing"),
    ServiceCategory(title="paint works"),
    ServiceCategory(title="tutoring"),
    ServiceCategory(title="water works"),
    ServiceCategory(title="wood work")
    ])
    
    db.session.add_all([Service(title="Chef booking",base_price=250,description="Enjoy delicious, freshly prepared meals in the comfort of your home with a professional chef.",category="catering")
    ,Service(title="Meal kits booking",base_price=200,description="Receive pre-portioned ingredients and recipes to create your own meals easily at home.",category="catering")
    ,Service(title="Full home cleaning",base_price=300,description="A thorough cleaning service to refresh and revitalize your entire home, ensuring a spotless environment.",category="cleaning")
    ,Service(title="Bathroom cleaning",base_price=180,description="Expert cleaning of your bathroom, focusing on hygiene and sanitation for a fresh space.",category="cleaning")
    ,Service(title="Kitchen cleaning",base_price=220,description="Deep cleaning service for your kitchen, ensuring a safe and sanitary cooking area.",category="cleaning")
    ,Service(title="Sofa-furniture cleaning",base_price=150,description="Revitalize your furniture with professional cleaning, removing dirt and allergens.",category="cleaning")
    ,Service(title="Home lighting",base_price=200,description="Expert installation and repair of home lighting to enhance your living space.",category="electric repairing")
    ,Service(title="Television repair",base_price=250,description="Professional repair services for your television to restore your viewing experience.",category="electric repairing")
    ,Service(title="Washing Machine repair",base_price=180,description="Efficient repair service for your washing machine to ensure it runs smoothly again.",category="electric repairing")
    ,Service(title="Air Conditioner Servicing",base_price=250,description="Keep your air conditioner running efficiently with expert servicing and maintenance.",category="electronic servicing")
    ,Service(title="Two wheeler Servicing",base_price=200,description="Comprehensive servicing for your two-wheeler to keep it in top condition.",category="electronic servicing")
    ,Service(title="Refrigerator Servicing",base_price=220,description="Professional servicing for your refrigerator to ensure optimal performance and longevity.",category="electronic servicing")
    ,Service(title="Birthday-Kitty party booking",base_price=250,description="Plan a fun and memorable birthday or kitty party with our professional event management services.",category="event management")
    ,Service(title="Tent Rental Services",base_price=300,description="Quality tent rental and setup services for your outdoor events, ensuring comfort and style.",category="event management")
    ,Service(title="Bathroom tile flooring",base_price=280,description="Expert installation of bathroom tiles, providing a stylish and durable flooring solution.",category="flooring")
    ,Service(title="Outdoors flooring",base_price=250,description="Installation of outdoor flooring options to enhance your garden or patio area.",category="flooring")
    ,Service(title="Garden management",base_price=200,description="Professional care and maintenance for your garden, ensuring it remains healthy and beautiful.",category="gardening")
    ,Service(title="Make up artist booking",base_price=220,description="Transform your look with professional makeup services for any occasion.",category="home beauty")
    ,Service(title="Massage therapist booking",base_price=250,description="Relax and unwind with a professional massage therapy session tailored to your needs.",category="gardening")
    ,Service(title="Home plaster fixing",base_price=180,description="Professional plaster fixing service to restore the beauty and integrity of your walls.",category="masonry")
    ,Service(title="Elderly Caretaker booking",base_price=300,description="Compassionate and professional care for the elderly in the comfort of their home.",category="nursing")
    ,Service(title="Babysitter booking",base_price=150,description="Reliable babysitting services to ensure your children are safe and cared for while you are away.",category="nursing")
    ,Service(title="Elementary school tutor booking",base_price=200,description="Personalized tutoring services for elementary students to enhance their learning experience.",category="tutoring")
    ,Service(title="High school tutor booking",base_price=250,description="Expert tutoring for high school students to help them excel in their studies.",category="tutoring")
    ,Service(title="Plumber for fixing",base_price=220,description="Professional plumbing services to quickly fix any leaks or plumbing issues in your home.",category="water works")])
    
    db.session.commit()
    print("----------------- Initial Entries Added! ----------------------\n")
    
print("----------------- Procedure completed! ----------------------\n\n")