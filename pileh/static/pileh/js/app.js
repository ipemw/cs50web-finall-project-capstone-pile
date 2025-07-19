document.addEventListener('DOMContentLoaded', function() {
    let productData = {};
    let modalHistory = [];
    let modalState = {
        type: '',
        data: [],
        searchQuery: ''
    };

    const brandInput = document.getElementById('brand');
    const modelInput = document.getElementById('model');
    const storageInput = document.getElementById('storage');
    const colorInput = document.getElementById('color');
    const simStatusInput = document.getElementById('simCardStatus');
    const productTitleInput = document.getElementById('productTitle');
    const addProductForm = document.getElementById('addProductForm');

    const hiddenBrandInput = document.getElementById('hidden_brand');
    const hiddenModelInput = document.getElementById('hidden_model');
    const hiddenStorageInput = document.getElementById('hidden_storage');
    const hiddenColorInput = document.getElementById('hidden_color');
    const hiddenSimStatusInput = document.getElementById('hidden_simCardStatus');

    const modal = document.getElementById('selectionModal');
    const modalLabel = document.getElementById('selectionModalLabel');
    const modalList = document.getElementById('modalList');
    const modalSearch = document.getElementById('modalSearch');
    const backBtn = document.getElementById('backBtn');

    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`);
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        const isDarkMode = localStorage.getItem('darkMode') === 'enabled';
        if (isDarkMode) {
            document.body.classList.add('dark-mode');
            darkModeToggle.innerHTML = '<i class="fa fa-sun-o"></i> Light Mode';
        } else {
            document.body.classList.remove('dark-mode');
            darkModeToggle.innerHTML = '<i class="fa fa-moon-o"></i> Dark Mode';
        }
        darkModeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-mode');
            const currentMode = document.body.classList.contains('dark-mode');
            localStorage.setItem('darkMode', currentMode ? 'enabled' : 'disabled');
            if (currentMode) {
                this.innerHTML = '<i class="fa fa-sun-o"></i> Light Mode';
            } else {
                this.innerHTML = '<i class="fa fa-moon-o"></i> Dark Mode';
            }
        });
    }

    window.submitEdit = function(productId) {
        const title = document.getElementById('edit_title').value;
        const price = document.getElementById('edit_price').value;
        const description = document.getElementById('edit_description').value;

        fetch(`/edit_product/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                title: title,
                price: price,
                description: description
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Could not update product.');
            }
            return response.json();
        })
        .then(result => {
            console.log('Success:', result);
            document.querySelector('.product-title').textContent = result.title;
            document.querySelector('.product-description').textContent = result.description;
            document.querySelector('.product-price').textContent = `Price: ${result.price} $`;
            $('#editModal').modal('hide');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Could not update product. Please try again.');
        });
    };

    window.deleteProduct = function(productId) {
        if (confirm('Are you sure you want to delete this product?')) {
            fetch(`/delete_product/${productId}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Could not delete product.');
                }
                window.location.href = '/';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Could not delete product. Please try again.');
            });
        }
    };

    window.toggleSold = function(productId) {
        fetch(`/mark_as_sold/${productId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Could not toggle sold status.');
            }
            return response.json();
        })
        .then(data => {
            const titleElement = document.querySelector('.product-title');
            const badgeHTML = `<span class="badge badge-danger">SOLD</span>`;

            if (data.is_sold) {
                if (!titleElement.querySelector('.badge')) {
                    titleElement.innerHTML += ' ' + badgeHTML;
                }
            } else {
                const badge = titleElement.querySelector('.badge');
                if (badge) {
                    badge.remove();
                }
            }

            const toggleLink = document.querySelector(`a[onclick="toggleSold('${productId}')"]`);
            if (toggleLink) {
                toggleLink.textContent = data.is_sold ? 'Mark as Available' : 'Mark as Sold';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Could not update status. Please try again.');
        });
    };

    let selectedBrand = null;
    let selectedSeries = null;
    let selectedModel = null;
    let selectedYear = null;
    let selectedStorage = null;
    let selectedColor = null;
    let productDataCache = {};

    function updateProductTitle() {
        let parts = [];
        if (brandInput && brandInput.value) parts.push(brandInput.value);
        if (modelInput && modelInput.value) parts.push(modelInput.value);
        if (colorInput && colorInput.value) parts.push(colorInput.value);
        if (storageInput && storageInput.value) parts.push(storageInput.value);
        if (productTitleInput) productTitleInput.value = parts.join(' ');
    }

    function populateModal(type, data, label) {
        modalState = { type: type, data: data, searchQuery: '' };
        modalLabel.textContent = label;
        modalSearch.value = '';
        populateModalList();
        if (backBtn) {
            backBtn.style.display = modalHistory.length > 0 ? 'inline-block' : 'none';
        }
        $(modal).modal('show');
    }

    function populateModalList() {
        modalList.innerHTML = '';
        const filteredData = filterData(modalState.data, modalState.searchQuery);
        filteredData.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item list-group-item-action';

            if (modalState.type === 'color') {
                li.style.display = 'flex';
                li.style.alignItems = 'center';
                li.style.gap = '10px';

                const colorSquare = document.createElement('div');
                colorSquare.style.width = '20px';
                colorSquare.style.height = '20px';
                colorSquare.style.backgroundColor = item.hex;
                colorSquare.style.border = '1px solid #ccc';
                colorSquare.style.borderRadius = '3px';

                const colorName = document.createElement('span');
                colorName.textContent = item.name;

                li.appendChild(colorSquare);
                li.appendChild(colorName);
                li.dataset.value = item.name;
            } else {
                li.textContent = item.name || item;
                li.dataset.value = item.name || item;
            }

            li.addEventListener('click', () => handleModalItemClick(item));
            modalList.appendChild(li);
        });
    }

    function filterData(data, query) {
        if (!data) return [];
        query = query.toLowerCase();
        if (query === '') return data;
        if (typeof data[0] === 'object') {
            return data.filter(item => item.name.toLowerCase().includes(query));
        }
        return data.filter(item => item.toLowerCase().includes(query));
    }
    
    function handleModalItemClick(item) {
        modalHistory.push({...modalState});
        
        switch (modalState.type) {
            case 'brand': {
                selectedBrand = item.name;
                brandInput.value = selectedBrand;
                if (hiddenBrandInput) hiddenBrandInput.value = selectedBrand;
                modelInput.value = '';
                if (hiddenModelInput) hiddenModelInput.value = '';
                storageInput.value = '';
                if (hiddenStorageInput) hiddenStorageInput.value = '';
                colorInput.value = '';
                if (hiddenColorInput) hiddenColorInput.value = '';
                simStatusInput.value = '';
                if (hiddenSimStatusInput) hiddenSimStatusInput.value = '';
                
                const brandObject = productDataCache.brands.find(b => b.name === selectedBrand);
                populateModal('series', brandObject.series, `Select a Series from ${selectedBrand}`);
                break;
            }
            case 'series': {
                const selectedSeriesObject = modalState.data.find(s => s.name === item.name);
                selectedSeries = selectedSeriesObject.name;
                storageInput.value = '';
                if (hiddenStorageInput) hiddenStorageInput.value = '';
                colorInput.value = '';
                if (hiddenColorInput) hiddenColorInput.value = '';
                simStatusInput.value = '';
                if (hiddenSimStatusInput) hiddenSimStatusInput.value = '';
                
                populateModal('model', selectedSeriesObject.models, `Select a Model from ${selectedSeries}`);
                break;
            }
            case 'model': {
                const selectedModelObject = modalState.data.find(m => m.name === item.name);
                selectedModel = selectedModelObject.name;
                modelInput.value = selectedModelObject.name;
                if (hiddenModelInput) hiddenModelInput.value = selectedModelObject.name;
                
                populateModal('storage', selectedModelObject.storages, `Select Storage for ${selectedModel}`);
                break;
            }
            case 'storage': {
                const selectedModelObject = productDataCache.brands.flatMap(b => b.series).flatMap(s => s.models).find(m => m.name === modelInput.value);
                selectedStorage = item;
                storageInput.value = selectedStorage;
                if (hiddenStorageInput) hiddenStorageInput.value = selectedStorage;
                
                populateModal('sim_status', selectedModelObject.sim_status, `Select SIM Card Status for ${selectedModel}`);
                break;
            }
            case 'sim_status': {
                selectedSimStatus = item;
                simStatusInput.value = selectedSimStatus;
                if (hiddenSimStatusInput) hiddenSimStatusInput.value = selectedSimStatus;

                const selectedModelObject = productDataCache.brands.flatMap(b => b.series).flatMap(s => s.models).find(m => m.name === modelInput.value);
                populateModal('color', selectedModelObject.colors, `Select Color for ${selectedModel}`);
                break;
            }
            case 'color': {
                selectedColor = item.name;
                colorInput.value = selectedColor;
                if (hiddenColorInput) hiddenColorInput.value = selectedColor;
                
                updateProductTitle();
                $(modal).modal('hide');
                break;
            }
        }
        if (backBtn) {
            backBtn.style.display = modalHistory.length > 0 ? 'inline-block' : 'none';
        }
    }
    
    if (brandInput) {
        brandInput.addEventListener('click', () => {
            modalHistory = [];
            populateModal('brand', productDataCache.brands, 'Select a Brand');
        });

        modelInput.addEventListener('click', () => {
            modalHistory = [];
            const brandObject = productDataCache.brands.find(b => b.name === brandInput.value);
            if (brandObject) {
                populateModal('series', brandObject.series, `Select a Series from ${brandInput.value}`);
            } else {
                alert('Please select a Brand first.');
            }
        });

        storageInput.addEventListener('click', () => {
            modalHistory = [];
            const selectedModelObject = productDataCache.brands.flatMap(b => b.series).flatMap(s => s.models).find(m => m.name === modelInput.value);
            if (selectedModelObject) {
                populateModal('storage', selectedModelObject.storages, `Select Storage for ${selectedModel}`);
            } else {
                alert('Please select a Model first.');
            }
        });
        
        colorInput.addEventListener('click', () => {
            modalHistory = [];
            const selectedModelObject = productDataCache.brands.flatMap(b => b.series).flatMap(s => s.models).find(m => m.name === modelInput.value);
            if (selectedModelObject) {
                populateModal('color', selectedModelObject.colors, `Select Color for ${selectedModel}`);
            } else {
                alert('Please select a Model first.');
            }
        });
        
        simStatusInput.addEventListener('click', () => {
            modalHistory = [];
            const selectedModelObject = productDataCache.brands.flatMap(b => b.series).flatMap(s => s.models).find(m => m.name === modelInput.value);
            if (selectedModelObject) {
                populateModal('sim_status', selectedModelObject.sim_status, 'Select SIM Card Status');
            } else {
                alert('Please select a Model first.');
            }
        });
    }

    if (backBtn) {
        backBtn.addEventListener('click', () => {
            if (modalHistory.length > 0) {
                const previousState = modalHistory.pop();
                modalState = previousState;
                modalLabel.textContent = `Select ${modalState.type === 'series' ? 'a Series from ' + brandInput.value : modalState.type === 'model' ? 'a Model from ' + selectedSeries : 'an Option'}`;
                populateModalList();
                backBtn.style.display = modalHistory.length > 0 ? 'inline-block' : 'none';
            }
        });
    }

    if (modalSearch) {
        modalSearch.addEventListener('input', () => {
            modalState.searchQuery = modalSearch.value.toLowerCase();
            populateModalList();
        });
    }

    if (addProductForm) {
        addProductForm.addEventListener('submit', function(event) {
            if (brandInput && hiddenBrandInput) hiddenBrandInput.value = brandInput.value;
            if (modelInput && hiddenModelInput) hiddenModelInput.value = modelInput.value;
            if (storageInput && hiddenStorageInput) hiddenStorageInput.value = storageInput.value;
            if (colorInput && hiddenColorInput) hiddenColorInput.value = colorInput.value;
            if (simStatusInput && hiddenSimStatusInput) hiddenSimStatusInput.value = simStatusInput.value;
        });
    }

    if (brandInput) {
        fetch('/get_product_data')
            .then(response => response.json())
            .then(data => {
                productDataCache = data;
            })
            .catch(error => console.error('Error fetching product data:', error));
    }
    
    if (brandInput) {
        brandInput.value = '';
        if (hiddenBrandInput) hiddenBrandInput.value = '';
        modelInput.value = '';
        if (hiddenModelInput) hiddenModelInput.value = '';
        storageInput.value = '';
        if (hiddenStorageInput) hiddenStorageInput.value = '';
        colorInput.value = '';
        if (hiddenColorInput) hiddenColorInput.value = '';
        simStatusInput.value = '';
        if (hiddenSimStatusInput) hiddenSimStatusInput.value = '';
        
    }

    // اضافه شدن این بخش برای کنترل فرم جستجو
    const searchForm = document.querySelector('.navbar .form-inline');
    const searchInput = document.querySelector('.navbar .form-inline input[type="search"]');

    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            if (searchInput.value.trim() === '') {
                event.preventDefault();
            }
        });
    }
});