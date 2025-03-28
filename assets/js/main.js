// 示範用嘅餐廳資料（實際上可以利用 fetch() 從 openrice_data.json 載入資料）
const restaurants = [
    { "name": "餐廳 A", "address": "香港中環XX街", "rating": 4.5 },
    { "name": "餐廳 B", "address": "九龍彌敦道XX號", "rating": 4.2 },
    { "name": "餐廳 C", "address": "新界沙田XX路", "rating": 4.7 },
    { "name": "餐廳 D", "address": "香港旺角XX大道", "rating": 4.0 },
    { "name": "餐廳 E", "address": "九龍尖沙咀XX街", "rating": 4.6 }
  ];
  
  // 模擬嘅菜單建議語句
  const menuAdvices = [
    "試下佢哋嘅招牌燒味！",
    "享受一份精緻嘅甜品以完美收官。",
    "點個招牌海鮮拼盤，絕對正！",
    "嚐試佢哋極受歡迎嘅意大利麵。",
    "今日來點道特色咖哩飯，暖心又滿足！"
  ];
  
  let filteredData = [...restaurants];
  
  // 生成餐廳卡片
  function generateRestaurantCards(data) {
    const grid = document.getElementById('restaurantGrid');
    grid.innerHTML = '';
    if (data.length === 0) {
      grid.innerHTML = `<p style="text-align:center; width:100%;">無符合條件嘅餐廳</p>`;
      return;
    }
    data.forEach(restaurant => {
      const card = document.createElement('div');
      card.className = 'restaurant-card';
      
      const header = document.createElement('header');
      header.textContent = restaurant.name;
      card.appendChild(header);
      
      const body = document.createElement('div');
      body.className = 'card-body';
      body.innerHTML = `
        <p><strong>地址：</strong> ${restaurant.address}</p>
        <p><strong>評分：</strong> ${restaurant.rating}</p>
        <a href="#" class="btn" onclick="alert('更多資訊功能未開放'); return false;">了解詳情</a>
      `;
      card.appendChild(body);
      
      const footer = document.createElement('div');
      footer.className = 'card-footer';
      footer.textContent = '美食推薦';
      card.appendChild(footer);
      
      grid.appendChild(card);
    });
  }
  
  // 搜尋、排序與篩選功能
  function filterRestaurants() {
    const searchQuery = document.getElementById('searchInput').value.toLowerCase();
    const sortBy = document.getElementById('sortBy').value;
    const filterRating = parseFloat(document.getElementById('filterRating').value);
  
    filteredData = restaurants.filter(restaurant => {
      const matchName = restaurant.name.toLowerCase().includes(searchQuery);
      const matchRating = restaurant.rating >= filterRating;
      return matchName && matchRating;
    });
  
    if (sortBy === 'ratingHigh') {
      filteredData.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === 'ratingLow') {
      filteredData.sort((a, b) => a.rating - b.rating);
    }
    generateRestaurantCards(filteredData);
  }
  
  // 隨機推薦功能
  function getRandomRecommendation() {
    if (restaurants.length === 0) return;
    const randomRestaurant = restaurants[Math.floor(Math.random() * restaurants.length)];
    const randomAdvice = menuAdvices[Math.floor(Math.random() * menuAdvices.length)];
    const resultDiv = document.getElementById('recommendationResult');
    resultDiv.style.display = 'block';
    resultDiv.innerHTML = `
      <h3 style="color:#B39DDB;">${randomRestaurant.name}</h3>
      <p><strong>地址：</strong>${randomRestaurant.address}</p>
      <p><strong>評分：</strong>${randomRestaurant.rating}</p>
      <p style="margin-top:10px; font-weight:600; color:#B39DDB;">今日推薦：${randomAdvice}</p>
    `;
    resultDiv.scrollIntoView({ behavior: "smooth" });
  }
  
  // 滾動到指定區塊（例如餐廳列表）
  function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: "smooth" });
  }
  
  // 頁面初始化
  window.onload = () => {
    generateRestaurantCards(restaurants);
  };