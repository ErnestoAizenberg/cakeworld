document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM fully loaded and parsed. Initializing...');
    init();
});

const csrfToken = document.querySelector('meta[name="csrf-token"]').content;
const headers = {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken
};

const errorDiv = document.createElement('div');
errorDiv.className = 'error';
document.querySelector('.container').prepend(errorDiv);

let editingItemId = null;  // Переменная для хранения ID редактируемого элемента

// Initialize functions and load items
function init() {
    console.log('Initializing functions and loading items...');
    fetchItems();
    setupFormSubmission();
}

function setupFormSubmission() {
    console.log('Setting up form submission handler...');
    document.getElementById('itemForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        console.log('Form submitted. Gathering item data...');

        const itemData = {
            name: document.getElementById('name').value.trim(),
            description: document.getElementById('description').value.trim(),
            image_url: document.getElementById('image_url').value.trim(),
            price_gems: parseInt(document.getElementById('price_gems').value),
            price_coins: parseInt(document.getElementById('price_coins').value),
            rarity: parseInt(document.getElementById('rarity').value)
        };

        // Проверка данных перед отправкой
        if (!validateItemData(itemData)) {
            showError('Please fill all fields correctly.');
            return;
        }

        console.log('Item data:', itemData);

        try {
            const method = editingItemId ? 'PUT' : 'POST';
            const url = editingItemId ? `/items/${editingItemId}` : '/items';

            const response = await fetch(url, {
                method: method,
                headers: headers,
                body: JSON.stringify(itemData),
                credentials: 'include'
            });

            console.log('Response from request:', response);
            
            if (!response.ok) {
                const errorResponse = await response.json();
                console.error('Error response from server:', errorResponse);
                if (errorResponse.details) {
                    const messages = errorResponse.details.map(error => `${error.field}: ${error.message}`).join(', ');
                    throw new Error(`Validation errors: ${messages}`);
                }
                throw new Error(errorResponse.message || 'Error submitting form');
            }

            console.log('Item successfully submitted. Fetching items...');
            fetchItems();
            e.target.reset();
            editingItemId = null;
        } catch (error) {
            console.error('Error during form submission:', error);
            showError(error.message || 'Error submitting form');
        }
    });
}

function validateItemData(itemData) {
    return itemData.name && itemData.description && itemData.image_url &&
           !isNaN(itemData.price_gems) && !isNaN(itemData.price_coins) && !isNaN(itemData.rarity);
}

async function fetchItems() {
    console.log('Fetching items...');
    try {
        const response = await fetch('/items');
        console.log('Response from GET /items:', response);
        
        if (!response.ok) {
            const errorResponse = await response.json();
            console.error('Error fetching items:', errorResponse);
            throw new Error(errorResponse.message || 'Error loading items');
        }

        const items = await response.json();
        console.log('Items received:', items);
        renderItems(items);
    } catch (error) {
        console.error('Error loading items:', error);
        showError('Error loading items');
    }
}

function renderItems(items) {
    console.log('Rendering items to the UI...');
    const container = document.getElementById('itemsContainer');
    container.innerHTML = items.map(item => `
        <div class="item-card" data-id="${item.id}">
            <div>
                <h3>${item.name}</h3>
                <p>${item.description}</p>
                <img src="${item.image_url}" alt="${item.name}" height="100">
                <p>Price: ${item.price_gems} gems, ${item.price_coins} coins</p>
                <p>Rarity: ${item.rarity}</p>
            </div>
            <div class="item-actions">
                <button onclick="editItem(${item.id})">Edit</button>
                <button class="delete-btn" onclick="deleteItem(${item.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function deleteItem(itemId) {
    console.log(`Attempting to delete item with ID: ${itemId}`);
    
    if (!confirm('Are you sure?')) {
        console.log('Item deletion cancelled by user.');
        return;
    }

    try {
        const response = await fetch(`/items/${itemId}`, {
            method: 'DELETE',
            headers: headers,
            credentials: 'include'
        });

        console.log('Response from DELETE /items/:', response);

        if (!response.ok) {
            const errorResponse = await response.json();
            console.error('Error response from server on delete:', errorResponse);
            throw new Error(errorResponse.message || 'Error deleting item');
        }

        console.log(`Item with ID ${itemId} successfully deleted. Fetching updated items...`);
        fetchItems();
    } catch (error) {
        console.error('Error deleting item:', error);
        showError(error.message || 'Error deleting item');
    }
}

async function editItem(itemId) {
    console.log(`Editing item with ID: ${itemId}`);
    editingItemId = itemId;

    try {
        const response = await fetch(`/items/${itemId}`);
        if (!response.ok) {
            const errorResponse = await response.json();
            console.error('Error response from server on edit:', errorResponse);
            throw new Error(errorResponse.message || 'Error fetching item for edit');
        }

        const item = await response.json();

        document.getElementById('name').value = item.name;
        document.getElementById('description').value = item.description;
        document.getElementById('image_url').value = item.image_url;
        document.getElementById('price_gems').value = item.price_gems;
        document.getElementById('price_coins').value = item.price_coins;
        document.getElementById('rarity').value = item.rarity;
    } catch (error) {
        console.error('Error fetching item for edit:', error);
        showError('Error fetching item details for editing');
    }
}

function showError(message) {
    console.error('Showing error message:', message);
    errorDiv.textContent = message;
    setTimeout(() => errorDiv.textContent = '', 3000);
}
