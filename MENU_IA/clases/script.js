document.addEventListener('DOMContentLoaded', () => {
    // Configuración
    const API_BASE_URL = "http://127.0.0.1:8000";
    let currentUserId = 1;
    let fullMenuData = [];
    let pendingRatings = {};

    // Referencias del DOM
    const onboardingView = document.getElementById('onboarding-view');
    const menuView = document.getElementById('menu-view');
    const detailView = document.getElementById('detail-view');
    const modalContent = document.querySelector('.modal-content');
    const closeButton = document.getElementById('close-detail');

    // Funciones API
    const fetchIngredients = async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/ingredientes`);
            return await response.json();
        } catch (error) {
            console.error("Error fetching ingredients:", error);
            throw error;
        }
    };

    const fetchMenu = async (userId) => {
        try {
            const response = await fetch(`${API_BASE_URL}/menu/${userId}`);
            return await response.json();
        } catch (error) {
            console.error("Error fetching menu:", error);
            throw error;
        }
    };

    const postRating = async (userId, ingredientId, score) => {
        try {
            await fetch(`${API_BASE_URL}/calificar_ingrediente`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    usuario_id: userId, 
                    ingrediente_id: ingredientId, 
                    puntuacion: score 
                })
            });
        } catch (error) {
            console.error("Error posting rating:", error);
            throw error;
        }
    };

    // Vistas
    const showView = (viewToShow) => {
        [onboardingView, menuView, detailView].forEach(v => v.style.display = 'none');
        viewToShow.style.display = 'block';
    };

    const renderOnboarding = async () => {
        try {
            const { ingredientes } = await fetchIngredients();
            const container = document.getElementById('onboarding-ingredients');
            container.innerHTML = '';
            
            ingredientes.forEach(ing => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.textContent = ing.nombre;
                tag.dataset.ingredientId = ing.id;
                tag.addEventListener('click', () => {
                    tag.classList.toggle('selected');
                    tag.style.animation = 'none';
                    setTimeout(() => {
                        tag.style.animation = 'fadeIn 0.3s ease';
                    }, 10);
                });
                container.appendChild(tag);
            });
        } catch (error) {
            console.error("No se pudieron cargar los ingredientes:", error);
            const container = document.getElementById('onboarding-ingredients');
            container.innerHTML = '<p style="color: #cf6679; text-align: center; padding: 20px;">Error: No se pudo conectar al servidor. Asegúrate de que el backend esté funcionando.</p>';
        }
    };

    document.getElementById('save-onboarding').addEventListener('click', async () => {
        const selectedTagsNodeList = document.querySelectorAll('#onboarding-ingredients .tag.selected');
        const selectedTagsArray = Array.from(selectedTagsNodeList);
        
        if (selectedTagsArray.length === 0) {
            alert('Por favor selecciona al menos un ingrediente que te guste.');
            return;
        }

        try {
            // Mostrar loading
            const button = document.getElementById('save-onboarding');
            const originalText = button.textContent;
            button.textContent = 'Guardando...';
            button.disabled = true;

            await Promise.all(selectedTagsArray.map(tag => {
                return postRating(currentUserId, tag.dataset.ingredientId, 5);
            }));

            localStorage.setItem(`onboarding_complete_user_${currentUserId}`, 'true');
            initMenu();
        } catch (error) {
            alert('Error al guardar las preferencias. Intenta nuevamente.');
            console.error(error);
        } finally {
            const button = document.getElementById('save-onboarding');
            button.textContent = originalText;
            button.disabled = false;
        }
    });

    // Flujo del menú
    const renderMenu = (data) => {
        fullMenuData = data.menu_completo;
        const container = document.getElementById('menu-content');
        container.innerHTML = `
            <div class="restaurant-header">
                <h1>WAJA SUCHI</h1>
            </div>
            <div class="menu-section">
                <h2>Recomendado para Ti <span class="recommendation-badge">:o</span></h2>
                <div id="recs-grid" class="menu-grid"></div>
            </div>
            <div class="menu-section">
                <h2>Menú Completo</h2>
                <div id="full-menu-grid" class="menu-grid"></div>
            </div>
        `;

        const recsGrid = document.getElementById('recs-grid');
        const fullMenuGrid = document.getElementById('full-menu-grid');

        // Renderizar recomendaciones
        if (data.recomendados && data.recomendados.length > 0) {
            data.recomendados.forEach(item => {
                recsGrid.appendChild(createMenuItem(item, true));
            });
        } else {
            recsGrid.innerHTML = '<p style="text-align: center; color: #888; grid-column: 1 / -1;">Califica más ingredientes para obtener recomendaciones personalizadas.</p>';
        }

        // Renderizar menú completo
        data.menu_completo.forEach(item => {
            fullMenuGrid.appendChild(createMenuItem(item, false));
        });
    };

    const createMenuItem = (item, isRecommended) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'menu-item';
        
        const probability = isRecommended ? item.probabilidad_recomendacion : null;
        
        itemDiv.innerHTML = `
            ${isRecommended && probability ? `<div class="probability">${probability}%</div>` : ''}
            <h3>${item.nombre}</h3>
            <div class="description">${item.descripcion || 'Deliciosa combinación de sabores únicos.'}</div>
            <div class="ingredients">${item.tipo_preparacion || 'Preparación especial'}</div>
        `;

        itemDiv.addEventListener('click', () => showDishDetail(item.nombre));
        return itemDiv;
    };

    const initMenu = async () => {
        showView(menuView);
        try {
            const menuData = await fetchMenu(currentUserId);
            renderMenu(menuData);
        } catch (error) {
            console.error("Error loading menu:", error);
            document.getElementById('menu-content').innerHTML = `
                <div style="text-align: center; color: #cf6679; padding: 50px;">
                    <h2>Error al cargar el menú</h2>
                    <p>No se pudo conectar al servidor. Verifica que el backend esté funcionando.</p>
                </div>
            `;
        }
    };

    // Modal de detalles
    const showDishDetail = (dishName) => {
        pendingRatings = {}; 
        const dish = fullMenuData.find(d => d.nombre === dishName);
        if (!dish) return;

        document.getElementById('detail-title').textContent = dish.nombre;
        document.getElementById('detail-description').textContent = dish.descripcion || 'Sin descripción disponible.';
        
        const ingredientsContainer = document.getElementById('detail-ingredients');
        ingredientsContainer.innerHTML = '';
        
        if (dish.ingredientes && dish.ingredientes.length > 0) {
            dish.ingredientes.forEach(ing => {
                const ingDiv = document.createElement('div');
                ingDiv.className = 'ingredient-rating';
                ingDiv.innerHTML = `<span>${ing.nombre}</span>`;
                const stars = createStarRating(ing.id);
                ingDiv.appendChild(stars);
                ingredientsContainer.appendChild(ingDiv);
            });
        } else {
            ingredientsContainer.innerHTML = '<p style="text-align: center; color: #888;">No hay información de ingredientes disponible.</p>';
        }

        detailView.style.display = 'flex';
    };

    const createStarRating = (ingredientId) => {
        const ratingDiv = document.createElement('div');
        ratingDiv.className = 'star-rating';
        
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.className = 'star';
            star.textContent = '★';
            star.dataset.score = i;
            star.addEventListener('click', () => {
                pendingRatings[ingredientId] = i;
                const allStars = ratingDiv.querySelectorAll('.star');
                allStars.forEach(s => {
                    s.classList.toggle('selected', s.dataset.score <= i);
                });
                
                // Efecto de animación
                star.style.animation = 'none';
                setTimeout(() => {
                    star.style.animation = 'fadeIn 0.3s ease';
                }, 10);
            });
            ratingDiv.appendChild(star);
        }
        return ratingDiv;
    };

    closeButton.addEventListener('click', async () => {
        if (Object.keys(pendingRatings).length > 0) {
            try {
                const ratingPromises = Object.entries(pendingRatings).map(([ingredientId, score]) => {
                    return postRating(currentUserId, ingredientId, score);
                });
                await Promise.all(ratingPromises);
                
                // Mostrar confirmación
                const button = closeButton;
                const originalText = button.textContent;
                button.textContent = '✓ Guardado';
                setTimeout(() => {
                    button.textContent = originalText;
                }, 2000);
            } catch (error) {
                alert('Error al guardar las calificaciones. Intenta nuevamente.');
                console.error(error);
            }
        }
        
        detailView.style.display = 'none';
        // Recargar el menú para actualizar recomendaciones
        initMenu();
    });

    modalContent.addEventListener('click', (event) => { 
        event.stopPropagation(); 
    });
    
    detailView.addEventListener('click', () => { 
        detailView.style.display = 'none'; 
    });

    // Manejar tecla Escape para cerrar modal
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && detailView.style.display === 'flex') {
            detailView.style.display = 'none';
        }
    });

    //INICIO
    const init = () => {
        if (localStorage.getItem(`onboarding_complete_user_${currentUserId}`)) {
            initMenu();
        } else {
            showView(onboardingView);
            renderOnboarding();
        }
    };

    init();
});