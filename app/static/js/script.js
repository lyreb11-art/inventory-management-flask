// Custom JavaScript for Inventory Management System

// Confirm delete actions
document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Add confirmation to delete buttons
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Format currency inputs
    const currencyInputs = document.querySelectorAll('input[type="number"][step="0.01"]');
    currencyInputs.forEach(function(input) {
        input.addEventListener('blur', function() {
            if (this.value) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    });
    
    // Search functionality enhancement
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.addEventListener('keyup', function(e) {
            if (e.key === 'Enter') {
                this.form.submit();
            }
        });
    }
    
    // Table row highlighting
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function(e) {
            if (e.target.tagName !== 'BUTTON' && e.target.tagName !== 'A') {
                this.classList.toggle('table-active');
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Print functionality
    const printButtons = document.querySelectorAll('.btn-print');
    printButtons.forEach(function(btn) {
        btn.addEventListener('click', function() {
            window.print();
        });
    });
});

// Helper function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Helper function to format date
function formatDate(date) {
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(new Date(date));
}

// Export table to CSV
function exportTableToCSV(filename) {
    const table = document.querySelector('table');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    rows.forEach(function(row) {
        let cols = row.querySelectorAll('td, th');
        let csvRow = [];
        cols.forEach(function(col) {
            csvRow.push('"' + col.textContent.trim() + '"');
        });
        csv.push(csvRow.join(','));
    });
    
    const csvContent = csv.join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}
