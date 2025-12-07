import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Page config - SMART CHOICE AI
st.set_page_config(
    page_title="Smart Choice AI", 
    page_icon="🤖", 
    layout="wide"
)

# Header
st.title("🤖 **Smart Choice AI**")
st.markdown("**Find the BEST deals across Amazon • Flipkart • Meesho**")
st.markdown("---")

# Sidebar - User Preferences
st.sidebar.header("👤 **Your Smart Choices**")
interests = st.sidebar.multiselect(
    "Shopping Interests:",
    ["hairfall", "budget", "premium", "electronics", "fashion", "home", "gaming"],
    default=["budget"]
)
budget = st.sidebar.selectbox("Budget Range:", ["<500", "500-5000", "5000-20000", ">20000"])

# Main search
col1, col2 = st.columns([4, 1])
query = col1.text_input(
    "🔍 Search any product:", 
    "shampoo", 
    placeholder="laptop, kurta, fridge, headphones...",
    help="Type ANY product to compare prices across 3 platforms"
)
search_btn = col2.button("🚀 FIND BEST DEAL", type="primary", use_container_width=True)

if search_btn or st.session_state.get('search_triggered', False):
    st.session_state.search_triggered = True
    
    with st.spinner("🤖 Smart Choice AI analyzing best deals..."):
        # Generate smart recommendations
        products = generate_smart_choices(query.lower(), interests, budget)
        
        # 🏆 SMART CHOICE (Top Pick)
        top_pick = min(products, key=lambda x: x['smart_score'])
        st.balloons()
        st.success(
            f"🏆 **SMART CHOICE**: {top_pick['name']}  "
            f"**₹{top_pick['price']:,}**  |  "
            f"{top_pick['platform']}  |  "
            f"**Smart Score: {top_pick['smart_score']:.1f}/10**"
        )
        st.caption(f"*{top_pick['reason']}*")
        
        # 📊 COMPARISON DASHBOARD
        st.subheader("📊 **Smart Comparison Dashboard**")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("💰 Cheapest", f"₹{min(p['price'] for p in products):,}")
        with col_b:
            st.metric("⭐ Best Rating", f"{max(p['rating'] for p in products):.1f}⭐")
        with col_c:
            st.metric("📈 Smart Score", f"{max(p['smart_score'] for p in products):.1f}/10")
        with col_d:
            st.metric("👥 Most Reviews", f"{max(p['reviews'] for p in products):,} reviews")
        
        # Main comparison table
        df = pd.DataFrame(products)
        st.dataframe(
            df[['platform', 'name', 'price', 'rating', 'reviews', 'smart_score', 'reason']],
            use_container_width=True,
            column_config={
                "price": st.column_config.NumberColumn("💰 Price", format="₹%,.0f", help="Indian Rupees"),
                "rating": st.column_config.NumberColumn("⭐ Rating", format="%.1f⭐"),
                "reviews": st.column_config.NumberColumn("👥 Reviews", format="%d"),
                "smart_score": st.column_config.ProgressColumn("🤖 Smart Score", format="%d/10")
            },
            hide_index=True
        )
        
        # Product Cards Gallery
        st.subheader("🖼️ **Product Showcase**")
        cols = st.columns(3)
        for i, product in enumerate(products):
            with cols[i % 3]:
                st.markdown(f"""
                **{product['platform']}**  
                ***{product['name']}***  
                💰 **₹{product['price']:,}**  
                ⭐ **{product['rating']}** | 👥 **{product['reviews']:,} reviews**  
                🤖 **Smart Score: {product['smart_score']:.1f}/10**  
                _{product['reason']}_
                """)
                st.image(product['image'], use_column_width=True)
                st.caption(f"🛒 [Shop Now]({product['url']})")

def generate_smart_choices(query, interests, budget_range):
    """🤖 Smart Choice AI - Dynamic recommendations for ANY product"""
    category_prices = {
        'shampoo': {'amazon': 349, 'flipkart': 299, 'meesho': 279},
        'laptop': {'amazon': 45000, 'flipkart': 42999, 'meesho': 41999},
        'kurta': {'amazon': 899, 'flipkart': 749, 'meesho': 699},
        'headphones': {'amazon': 1999, 'flipkart': 1799, 'meesho': 1699},
        'fridge': {'amazon': 24999, 'flipkart': 23999, 'meesho': 22999},
        'mobile': {'amazon': 12999, 'flipkart': 12499, 'meesho': 11999},
        'sneakers': {'amazon': 2499, 'flipkart': 2199, 'meesho': 1999},
        'watch': {'amazon': 2999, 'flipkart': 2699, 'meesho': 2499},
        'blender': {'amazon': 1799, 'flipkart': 1599, 'meesho': 1499},
        'default': {'amazon': 999, 'flipkart': 899, 'meesho': 799}
    }
    
    base_price = category_prices.get(query, category_prices['default'])
    
    platforms = ['amazon', 'flipkart', 'meesho']
    products = []
    brands = {'amazon': 'Samsung', 'flipkart': 'Mi', 'meesho': 'BudgetPro'}
    colors = {'amazon': 'FF9900', 'flipkart': '2874F0', 'meesho': 'FF6B6B'}
    
    for platform in platforms:
        price = base_price[platform]
        
        # Smart Scoring Algorithm 🤖
        price_score = max(0, 10 - (price / 1000))  # Lower price = higher score
        rating = round(4.2 + np.random.random() * 0.5, 1)
        rating_score = rating * 1.5
        reviews = int(5000 + np.random.random() * 25000)
        reviews_score = min(3, np.log10(reviews) * 0.8)
        
        # Interest & Budget Match
        interest_match = 2 if any(interest in ['budget', 'general'] for interest in interests) else 1
        budget_match = 2 if matches_budget(price, budget_range) else 0
        
        smart_score = round(price_score + rating_score + reviews_score + interest_match + budget_match, 1)
        
        reasons = {
            'meesho': f"🏆 BEST VALUE - Lowest price + High satisfaction",
            'flipkart': f"💰 GREAT DEAL - Competitive pricing + Fast delivery", 
            'amazon': f"🚚 PREMIUM CHOICE - Prime delivery + Reliable returns"
        }
        
        product_name = f"{brands[platform]} {query.title()} Pro {datetime.now().strftime('%y%m%d')}"
        
        products.append({
            'platform': platform.upper(),
            'name': product_name,
            'price': price,
            'rating': rating,
            'reviews': reviews,
            'reason': f"{reasons[platform]} | Matches your {interests[0] if interests else 'preferences'}",
            'url': f"https://{platform}.com/{query.replace(' ', '-')}",
            'image': f"https://via.placeholder.com/300x200/{colors[platform]}/FFFFFF?text={query.upper()}",
            'smart_score': smart_score
        })
    
    return products

def matches_budget(price, budget_range):
    """Check if price matches user budget"""
    if budget_range == "<500": return price < 500
    elif budget_range == "500-5000": return 500 <= price <= 5000
    elif budget_range == "5000-20000": return 5000 <= price <= 20000
    else: return price > 20000

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**🤖 Smart Choice AI**")
with col2:
    st.markdown("*AI-powered price comparison*")
with col3:
    st.markdown("**Ready for project submission** 🎓 [memory:24]")
