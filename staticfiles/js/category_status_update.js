document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.status-form select').forEach(select => {
        select.addEventListener('change', function() {
            const form = this.closest('form');
            const categoryId = form.dataset.categoryId;
            const status = this.value;

            fetch(`/categories/${categoryId}/update_status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ status })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Status updated successfully');
                } else {
                    alert('Failed to update status');
                }
            });
        });
    });
});