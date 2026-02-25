/* ===== AB Construction Ltd - Main JavaScript ===== */

// ===== Mobile Navigation =====
document.addEventListener('DOMContentLoaded', function() {
  const menuToggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  
  if (menuToggle) {
    menuToggle.addEventListener('click', function() {
      nav.classList.toggle('open');
    });
  }

  // Dropdown toggle on mobile
  document.querySelectorAll('.nav-list > li').forEach(function(item) {
    if (item.querySelector('.dropdown')) {
      item.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
          item.classList.toggle('dropdown-open');
        }
      });
    }
  });

  // Close menu on link click
  document.querySelectorAll('.nav-list a').forEach(function(link) {
    link.addEventListener('click', function() {
      if (window.innerWidth <= 768 && !link.parentElement.querySelector('.dropdown')) {
        nav.classList.remove('open');
      }
    });
  });

  // Scroll animations
  const fadeElements = document.querySelectorAll('.fade-in');
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });

  fadeElements.forEach(function(el) {
    observer.observe(el);
  });

  // Counter animation
  const counters = document.querySelectorAll('.counter');
  const counterObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        const target = parseInt(entry.target.getAttribute('data-target'));
        const suffix = entry.target.getAttribute('data-suffix') || '';
        animateCounter(entry.target, target, suffix);
        counterObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(function(counter) {
    counterObserver.observe(counter);
  });
});

function animateCounter(element, target, suffix) {
  let current = 0;
  const increment = target / 60;
  const timer = setInterval(function() {
    current += increment;
    if (current >= target) {
      current = target;
      clearInterval(timer);
    }
    element.textContent = Math.floor(current) + suffix;
  }, 30);
}

// ===== Lead Storage (localStorage) =====
function saveLeadToStorage(leadData) {
  let leads = JSON.parse(localStorage.getItem('ab_construction_leads') || '[]');
  leadData.id = Date.now();
  leadData.date = new Date().toISOString();
  leadData.status = 'new';
  leads.unshift(leadData);
  localStorage.setItem('ab_construction_leads', JSON.stringify(leads));
  return true;
}

function getLeadsFromStorage() {
  return JSON.parse(localStorage.getItem('ab_construction_leads') || '[]');
}

// ===== Form Handling =====
function initContactForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return;

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const formData = new FormData(form);
    const leadData = {};
    formData.forEach(function(value, key) {
      if (key !== 'access_key' && key !== 'botcheck' && key !== 'subject') {
        leadData[key] = value;
      }
    });

    // Save to localStorage
    saveLeadToStorage(leadData);

    // Submit to FormSubmit.co
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    fetch(form.action, {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      }
    }).then(function(response) {
      if (response.ok) {
        showFormSuccess(form);
      } else {
        // Still show success since we saved locally
        showFormSuccess(form);
      }
    }).catch(function() {
      // Still show success since we saved locally
      showFormSuccess(form);
    }).finally(function() {
      submitBtn.textContent = originalText;
      submitBtn.disabled = false;
    });
  });
}

function showFormSuccess(form) {
  form.style.display = 'none';
  const successDiv = form.parentElement.querySelector('.form-success');
  if (successDiv) {
    successDiv.classList.add('show');
    setTimeout(function() {
      form.style.display = 'block';
      form.reset();
      successDiv.classList.remove('show');
    }, 5000);
  }
}

// Initialize all forms on page
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.lead-capture-form').forEach(function(form) {
    initContactForm(form.id);
  });
});

// ===== AI Sales Chatbot =====
const ChatBot = {
  isOpen: false,
  messages: [],
  currentStep: 'greeting',
  leadData: {},

  responses: {
    greeting: {
      text: "Hello! Welcome to AB Construction Ltd. We're Swadlincote's trusted builders with years of experience. How can I help you today?",
      options: [
        { text: "Get a Free Quote", next: "quote_service" },
        { text: "View Our Services", next: "services_list" },
        { text: "Contact Us", next: "contact_info" },
        { text: "Why Choose Us?", next: "why_us" }
      ]
    },
    quote_service: {
      text: "Great choice! A free, no-obligation quote is the best way to start. Which service are you interested in?",
      options: [
        { text: "Brickwork", next: "quote_details" },
        { text: "Joinery", next: "quote_details" },
        { text: "Extensions", next: "quote_details" },
        { text: "Loft Conversions", next: "quote_details" },
        { text: "Kitchens", next: "quote_details" },
        { text: "Bathrooms", next: "quote_details" },
        { text: "Renovation Works", next: "quote_details" }
      ]
    },
    services_list: {
      text: "We offer a comprehensive range of construction services:\n\n🧱 **Brickwork** - Expert bricklaying & stonework\n🪚 **Joinery** - Custom woodwork & carpentry\n🏠 **Extensions** - Home extensions of all sizes\n🏗️ **Loft Conversions** - Maximize your space\n🍳 **Kitchens** - Dream kitchen installations\n🛁 **Bathrooms** - Luxury bathroom fitting\n🔨 **Renovation Works** - Full property renovations\n\nWhich service interests you most?",
      options: [
        { text: "Get a Free Quote", next: "quote_service" },
        { text: "Tell Me About Extensions", next: "extensions_info" },
        { text: "Tell Me About Loft Conversions", next: "loft_info" },
        { text: "Contact Us", next: "contact_info" }
      ]
    },
    extensions_info: {
      text: "Our home extensions are one of our most popular services! We handle everything from planning permission to the final finish. Whether you need a single-storey rear extension, a two-storey side extension, or a wraparound extension, we deliver exceptional quality.\n\nMost clients see a 15-20% increase in property value with a well-designed extension. Shall I arrange a free site visit?",
      options: [
        { text: "Yes, Get a Free Quote!", next: "quote_details" },
        { text: "How Much Does It Cost?", next: "cost_info" },
        { text: "View Other Services", next: "services_list" }
      ]
    },
    loft_info: {
      text: "Loft conversions are one of the best ways to add value and space to your home! We specialise in:\n\n- Dormer loft conversions\n- Hip-to-gable conversions\n- Velux/rooflight conversions\n- L-shaped loft conversions\n\nA loft conversion can add up to 20% to your property value and gives you that extra bedroom, office, or living space you need. Want to discuss your project?",
      options: [
        { text: "Yes, Get a Free Quote!", next: "quote_details" },
        { text: "How Long Does It Take?", next: "timeline_info" },
        { text: "View Other Services", next: "services_list" }
      ]
    },
    cost_info: {
      text: "Every project is unique, so we provide tailored quotes rather than one-size-fits-all pricing. This ensures you get the best value for your specific requirements.\n\nThe good news? Our quotes are completely FREE with no obligation. We'll visit your property, discuss your vision, and provide a detailed, transparent quote.\n\nShall I arrange this for you?",
      options: [
        { text: "Yes, Arrange a Free Quote!", next: "quote_details" },
        { text: "Contact Us Directly", next: "contact_info" }
      ]
    },
    timeline_info: {
      text: "Timelines vary depending on the project scope, but here's a rough guide:\n\n- Bathroom: 2-4 weeks\n- Kitchen: 3-6 weeks\n- Extension: 8-16 weeks\n- Loft Conversion: 6-10 weeks\n- Full Renovation: 12-24 weeks\n\nWe always provide a detailed timeline before starting and keep you updated throughout. Ready to get started?",
      options: [
        { text: "Get a Free Quote!", next: "quote_details" },
        { text: "Contact Us", next: "contact_info" }
      ]
    },
    why_us: {
      text: "Here's why Swadlincote trusts AB Construction Ltd:\n\n✅ Experienced, skilled tradesmen\n✅ Fully insured & certified\n✅ Free, no-obligation quotes\n✅ Transparent pricing - no hidden costs\n✅ Quality materials & workmanship\n✅ Clean, tidy, and professional\n✅ Excellent local reputation\n✅ Projects completed on time & budget\n\nWe're not just builders - we're your neighbours, and our reputation matters to us!",
      options: [
        { text: "Get a Free Quote", next: "quote_service" },
        { text: "View Services", next: "services_list" },
        { text: "Contact Us", next: "contact_info" }
      ]
    },
    quote_details: {
      text: "Excellent! To arrange your free quote, I just need a few details. What's your name?",
      options: [],
      input: "name"
    },
    ask_phone: {
      text: "Thanks, {name}! What's the best phone number to reach you on?",
      options: [],
      input: "phone"
    },
    ask_email: {
      text: "And your email address?",
      options: [],
      input: "email"
    },
    ask_message: {
      text: "Finally, could you briefly describe what you're looking for? (e.g., 'rear extension for kitchen', 'loft conversion to bedroom')",
      options: [],
      input: "message"
    },
    quote_submitted: {
      text: "Thank you, {name}! Your enquiry has been submitted successfully. 🎉\n\nOne of our team will be in touch within 24 hours to discuss your project and arrange a free site visit.\n\nIn the meantime, you can also call us directly:\n📞 01283 310115\n📞 07710 280062\n\nWe look forward to helping you with your project!",
      options: [
        { text: "View Our Services", next: "services_list" },
        { text: "Start Over", next: "greeting" }
      ]
    },
    contact_info: {
      text: "We'd love to hear from you! Here's how to reach us:\n\n📞 **Phone:** 01283 310115\n📱 **Mobile:** 07710 280062\n📍 **Location:** Swadlincote, UK\n\nOr fill out the contact form on any of our pages and we'll get back to you within 24 hours.\n\nWould you like a free quote instead?",
      options: [
        { text: "Get a Free Quote", next: "quote_service" },
        { text: "View Services", next: "services_list" },
        { text: "Start Over", next: "greeting" }
      ]
    }
  },

  init: function() {
    this.createElements();
    this.bindEvents();
    // Auto-show greeting after 3 seconds
    setTimeout(function() {
      const badge = document.querySelector('.chatbot-toggle .badge');
      if (badge) badge.style.display = 'flex';
    }, 3000);
  },

  createElements: function() {
    // Toggle button
    const toggle = document.createElement('button');
    toggle.className = 'chatbot-toggle';
    toggle.innerHTML = '💬 <span class="badge" style="display:none">1</span>';
    toggle.setAttribute('aria-label', 'Open chat');
    document.body.appendChild(toggle);

    // Chat window
    const window = document.createElement('div');
    window.className = 'chatbot-window';
    window.innerHTML = `
      <div class="chatbot-header">
        <div>
          <h4>AB Construction Assistant</h4>
          <div class="status">● Online - Ready to help</div>
        </div>
        <button class="chatbot-close" aria-label="Close chat">&times;</button>
      </div>
      <div class="chatbot-messages" id="chatMessages"></div>
      <div class="chatbot-input">
        <input type="text" id="chatInput" placeholder="Type your message..." />
        <button id="chatSend" aria-label="Send message">➤</button>
      </div>
    `;
    document.body.appendChild(window);
  },

  bindEvents: function() {
    const self = this;
    
    document.querySelector('.chatbot-toggle').addEventListener('click', function() {
      self.toggle();
    });

    document.querySelector('.chatbot-close').addEventListener('click', function() {
      self.close();
    });

    document.getElementById('chatSend').addEventListener('click', function() {
      self.sendUserMessage();
    });

    document.getElementById('chatInput').addEventListener('keypress', function(e) {
      if (e.key === 'Enter') self.sendUserMessage();
    });
  },

  toggle: function() {
    if (this.isOpen) {
      this.close();
    } else {
      this.open();
    }
  },

  open: function() {
    this.isOpen = true;
    document.querySelector('.chatbot-window').classList.add('open');
    document.querySelector('.chatbot-toggle .badge').style.display = 'none';
    if (this.messages.length === 0) {
      this.showResponse('greeting');
    }
  },

  close: function() {
    this.isOpen = false;
    document.querySelector('.chatbot-window').classList.remove('open');
  },

  addMessage: function(text, type) {
    const messagesDiv = document.getElementById('chatMessages');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'chat-message ' + type;
    // Convert markdown-style bold and newlines
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    text = text.replace(/\n/g, '<br>');
    msgDiv.innerHTML = text;
    messagesDiv.appendChild(msgDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    this.messages.push({ text: text, type: type });
  },

  showResponse: function(step) {
    const self = this;
    this.currentStep = step;
    const response = this.responses[step];
    if (!response) return;

    let text = response.text;
    // Replace placeholders
    text = text.replace('{name}', this.leadData.name || 'there');

    setTimeout(function() {
      self.addMessage(text, 'bot');

      if (response.options && response.options.length > 0) {
        const messagesDiv = document.getElementById('chatMessages');
        const optionsDiv = document.createElement('div');
        optionsDiv.className = 'chat-options';
        
        response.options.forEach(function(option) {
          const btn = document.createElement('button');
          btn.className = 'chat-option-btn';
          btn.textContent = option.text;
          btn.addEventListener('click', function() {
            self.addMessage(option.text, 'user');
            // Store service selection if in quote flow
            if (step === 'quote_service') {
              self.leadData.service = option.text;
            }
            optionsDiv.remove();
            self.showResponse(option.next);
          });
          optionsDiv.appendChild(btn);
        });

        messagesDiv.appendChild(optionsDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      }

      // Show/hide input based on whether we need text input
      const inputDiv = document.querySelector('.chatbot-input');
      if (response.input) {
        inputDiv.style.display = 'flex';
        document.getElementById('chatInput').focus();
      }
    }, 500);
  },

  sendUserMessage: function() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    this.addMessage(text, 'user');
    input.value = '';

    const response = this.responses[this.currentStep];
    
    if (response && response.input) {
      this.leadData[response.input] = text;
      
      // Progress through quote flow
      if (response.input === 'name') {
        this.showResponse('ask_phone');
      } else if (response.input === 'phone') {
        this.showResponse('ask_email');
      } else if (response.input === 'email') {
        this.showResponse('ask_message');
      } else if (response.input === 'message') {
        // Save the lead
        saveLeadToStorage(this.leadData);
        this.showResponse('quote_submitted');
        // Reset lead data for next conversation
        this.leadData = {};
      }
    } else {
      // Free text - try to match intent
      this.handleFreeText(text);
    }
  },

  handleFreeText: function(text) {
    const lower = text.toLowerCase();
    
    if (lower.includes('quote') || lower.includes('price') || lower.includes('cost') || lower.includes('estimate')) {
      this.showResponse('quote_service');
    } else if (lower.includes('service') || lower.includes('what do you')) {
      this.showResponse('services_list');
    } else if (lower.includes('contact') || lower.includes('phone') || lower.includes('call') || lower.includes('email')) {
      this.showResponse('contact_info');
    } else if (lower.includes('extension')) {
      this.showResponse('extensions_info');
    } else if (lower.includes('loft')) {
      this.showResponse('loft_info');
    } else if (lower.includes('why') || lower.includes('choose') || lower.includes('trust')) {
      this.showResponse('why_us');
    } else if (lower.includes('how long') || lower.includes('time') || lower.includes('timeline')) {
      this.showResponse('timeline_info');
    } else if (lower.includes('brick')) {
      this.leadData.service = 'Brickwork';
      this.showResponse('quote_details');
    } else if (lower.includes('joiner') || lower.includes('wood') || lower.includes('carpent')) {
      this.leadData.service = 'Joinery';
      this.showResponse('quote_details');
    } else if (lower.includes('kitchen')) {
      this.leadData.service = 'Kitchens';
      this.showResponse('quote_details');
    } else if (lower.includes('bathroom')) {
      this.leadData.service = 'Bathrooms';
      this.showResponse('quote_details');
    } else if (lower.includes('renovat') || lower.includes('refurb')) {
      this.leadData.service = 'Renovation Works';
      this.showResponse('quote_details');
    } else {
      this.addMessage("I'd love to help! Here are some things I can assist with:", 'bot');
      this.showResponse('greeting');
    }
  }
};

// Initialize chatbot when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
  ChatBot.init();
});
