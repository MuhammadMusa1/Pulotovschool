// script.js
document.addEventListener('DOMContentLoaded', function() {
    // Sticky header
    const header = document.getElementById('header');
    const hero = document.getElementById('hero');
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > hero.offsetHeight / 3) {
            header.classList.add('sticky');
        } else {
            header.classList.remove('sticky');
        }
    });
    
    // Fade-in animations on scroll
    const fadeElements = document.querySelectorAll('.fade-up, .animate-on-scroll');
    
    function checkFade() {
        fadeElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < window.innerHeight - elementVisible) {
                element.classList.add('visible');
            }
        });
    }
    
    // Initial check
    checkFade();
    
    // Check on scroll
    window.addEventListener('scroll', checkFade);
    
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileNav = document.getElementById('mobile-nav');
    
    mobileMenuBtn.addEventListener('click', function() {
        mobileNav.classList.toggle('open');
    });
    
    function closeMobileMenu() {
        mobileNav.classList.remove('open');
    }
    
    // Testimonial slider
    const dots = document.querySelectorAll('.dot');
    const testimonialCard = document.getElementById('testimonial-card');
    
    dots.forEach(dot => {
        dot.addEventListener('click', function() {
            const index = this.getAttribute('data-index');
            
            // Update active dot
            dots.forEach(d => d.classList.remove('active'));
            this.classList.add('active');
            
            // Update testimonial content based on index
            const testimonials = [
                {
                    text: "Дочь теперь каждый день хочет заниматься робототехникой! После первого занятия она сказала: 'Мама, я хочу создать робота, который будет мыть посуду!' Преподаватели действительно знают, как вдохновить детей.",
                    name: "Анна Петрова",
                    child: "Мария, 13 лет",
                    avatar: "https://placehold.co/60x60/4f46e5/ffffff?text=АП"
                },
                {
                    text: "Сын прошел два курса и уже участвовал в двух олимпиадах по робототехнике. Получил призовые места и теперь мечтает поступить в МФТИ. Отличная школа для подготовки к IT-будущему!",
                    name: "Игорь Сидоров",
                    child: "Даниил, 16 лет",
                    avatar: "https://placehold.co/60x60/059669/ffffff?text=ИС"
                },
                {
                    text: "Раньше дочка сидела только за планшетом, а теперь сама собирает роботов и пишет код! Занятия проходят в безопасной и дружеской атмосфере — это главное для меня как родителя.",
                    name: "Екатерина Волкова",
                    child: "Лиза, 11 лет",
                    avatar: "https://placehold.co/60x60/dc2626/ffffff?text=ЕВ"
                },
                {
                    text: "Наши команды выиграли турнир роботов в Москве! Никогда не думал, что сын сможет так увлечься программированием. Теперь он мечтает стать инженером-робототехником.",
                    name: "Максим Кузнецов",
                    child: "Артем, 15 лет",
                    avatar: "https://placehold.co/60x60/7c3aed/ffffff?text=МК"
                }
            ];
            
            testimonialCard.innerHTML = `
                <p class="testimonial-text">${testimonials[index].text}</p>
                <div class="testimonial-author">
                    <img src="${testimonials[index].avatar}" alt="${testimonials[index].name}" class="author-avatar">
                    <div class="author-info">
                        <h4>${testimonials[index].name}</h4>
                        <p>${testimonials[index].child}</p>
                    </div>
                </div>
            `;
        });
    });
    
    // Form validation and submission
    const form = document.getElementById('registration-form');
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.textContent = 'Заявка успешно отправлена! Мы свяжемся с вами в течение 15 минут.';
    document.body.appendChild(successMessage);
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Reset errors
        document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
        
        let isValid = true;
        
        // Validate child name
        const childName = document.getElementById('child-name').value.trim();
        if (!childName) {
            document.getElementById('child-name-error').textContent = 'Введите имя ребенка';
            isValid = false;
        }
        
        // Validate age
        const age = document.getElementById('age').value;
        if (!age || age < 10 || age > 17) {
            document.getElementById('age-error').textContent = 'Возраст должен быть от 10 до 17 лет';
            isValid = false;
        }
        
        // Validate phone
        const phone = document.getElementById('phone').value.trim();
        const phoneRegex = /^[\+]?[78]?[-\s]?(\(?\d{3}\)?[-\s]?){2}\d{4}$/;
        if (!phone) {
            document.getElementById('phone-error').textContent = 'Введите номер телефона';
            isValid = false;
        } else if (!phoneRegex.test(phone.replace(/\D/g, ''))) {
            document.getElementById('phone-error').textContent = 'Неверный формат телефона';
            isValid = false;
        }
        
        // Validate email (optional)
        const email = document.getElementById('email').value.trim();
        if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            document.getElementById('email-error').textContent = 'Неверный формат email';
            isValid = false;
        }
        
        if (isValid) {
            // Show success message
            successMessage.classList.add('show');
            
            // Clear form
            form.reset();
            
            // Hide success message after 3 seconds
            setTimeout(() => {
                successMessage.classList.remove('show');
            }, 3000);
        }
    });
    
    // Phone input formatting
    const phoneInput = document.getElementById('phone');
    
    phoneInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        
        if (value.length === 0) {
            e.target.value = '';
            return;
        }
        
        if (value.length <= 3) {
            e.target.value = value;
        } else if (value.length <= 6) {
            e.target.value = `+7 (${value.slice(0, 3)}) ${value.slice(3)}`;
        } else {
            e.target.value = `+7 (${value.slice(0, 3)}) ${value.slice(3, 6)}-${value.slice(6, 8)}-${value.slice(8, 10)}`;
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (mobileNav.classList.contains('open')) {
                    mobileNav.classList.remove('open');
                }
            }
        });
    });
    
    // CTA button click tracking
    document.querySelector('.cta-button').addEventListener('click', function() {
        // This would typically send data to analytics
        console.log('CTA button clicked - conversion tracked');
    });
});