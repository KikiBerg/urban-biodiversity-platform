$(document).ready(function() {
    $('.vote-btn').click(function() {
        var button = $(this);
        var postId = button.data('post-id');
        var voteType = button.data('vote-type');
        var csrftoken = '{{ csrf_token }}';

        $.ajax({
            url: '{% url "vote_post" post_id=0 %}'.replace('0', postId),
            type: 'POST',
            data: {
                'vote_type': voteType,
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                $('.upvote-count').text(response.upvotes);
                $('.downvote-count').text(response.downvotes);
                console.log('Vote successful');
            },
            error: function(xhr, status, error) {
                console.error('Error voting:', error);
                alert('There was an error processing your vote. Please try again.');
            }
        });
    });
});