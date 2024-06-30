$(document).ready(function() {
    console.log('Document ready');
    $('.vote-btn').click(function(e) {
        e.preventDefault();
        var button = $(this);
        var postId = button.data('post-id');
        var voteType = button.data('vote-type');
        console.log('Button clicked:', voteType, 'for post', postId);

        $.ajax({
            url: '/vote/' + postId + '/',
            type: 'POST',
            data: {
                'vote_type': voteType,
                'csrfmiddlewaretoken': '{{ csrf_token }}'
            },
            success: function(response) {
                console.log('Vote successful:', response);
                $('.upvote-count').text(response.upvotes);
                $('.downvote-count').text(response.downvotes);
                $('#debug-upvotes').text(response.upvotes);
                $('#debug-downvotes').text(response.downvotes);
            },
            error: function(xhr, status, error) {
                console.error('Vote failed:', status, error);
                console.log('Response:', xhr.responseText);
            }
        });
    });
});