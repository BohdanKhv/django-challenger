// ------------------- AJAX TEST ----------------------------------------
var followForm = document.querySelector('.followToggleForm'),
    commentForm = document.querySelector('.commentForm'),
    deleteCommentForm = document.getElementsByClassName('deleteCommentForm'),
    commentField = document.querySelector('.ajax-comment');

if(followForm){
    followForm.addEventListener('click', function(e){

        e.preventDefault();

        var followPK = followForm.dataset.pk;
        var url = followForm.href;

        var data = 'pk=' + followPK;

        var Xhr = new XMLHttpRequest();
        Xhr.open( 'GET', url, true );
        Xhr.setRequestHeader( 'Content-type','application/x-www-form-urlencoded' );

        Xhr.onload = function() {
            if ( this.status == 200 ) {
                if(followForm.textContent == 'Follow'){
                    followForm.classList.toggle('btn-outline-danger');
                    followForm.classList.toggle('btn-outline-info');
                    followForm.textContent = 'Unfollow';
                } else {
                    followForm.classList.toggle('btn-outline-danger');
                    followForm.classList.toggle('btn-outline-info');
                    followForm.textContent = 'Follow';
                }
            }
        }
        Xhr.send( data );

    });
}

if(commentForm){
    commentForm.addEventListener('submit', function(e){

        e.preventDefault();

        var comment = document.querySelector('#id_comment');
        var csrf = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        var url = commentForm.action;

        var data = 'csrfmiddlewaretoken=' + csrf +'&comment=' + comment.value;

        var Xhr = new XMLHttpRequest();
        Xhr.open( 'POST', url, false );
        Xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");

        Xhr.onload = function(e) {
            if ( this.status == 200 ) {
                var jsonComment = JSON.parse(this.responseText);
                console.log(jsonComment)
                commentField.innerHTML += '<div class="row justify-content-center">' +
                        '<div class="col-3">' +
                            '<div class="avatar text-center">' +
                                '<div style="background-image: URL(/media/'+userImg+'); width: 60px; height: 60px;" class="profile-photo rounded-circle">' +
                                '</div>' + 
                            '</div>' +
                        '</div>' +
                        '<div class="col-9 pl-md-0">' +
                            '<h6 class="mb-0">' +
                                '<a class="text-light" href="/user-profile/'+ jsonComment[0].fields.user +'">' + user + '</a>' +
                            '</h6>' +
                            '<small class="text-info">' +
                                'Just now' +
                            '</small>' +
                            '<p>' + jsonComment[0].fields.comment +
                            '</p>' +
                        '</div>' +
                    '</div>' +
                '<hr>'
                comment.value = '';
            }
        }
        Xhr.send( data );

    });

    
    for(let i = 0; i < deleteCommentForm.length; i++){
        deleteCommentForm[i].addEventListener('click', function(e){

            e.preventDefault();

            let deleteBtn = this;
            var commentPk = this.dataset.commentPk;
            var url = this.href;

            var data = 'pk=' + commentPk;

            var Xhr = new XMLHttpRequest();
            Xhr.open( 'GET', url, true );
            Xhr.setRequestHeader( 'Content-type','application/x-www-form-urlencoded' );

            Xhr.onload = function() {
                if ( this.status == 200 ) {
                    deleteBtn.offsetParent.parentNode.classList.add('opacity-zero');
                    deleteBtn.offsetParent.parentNode.addEventListener('transitionend', function(){
                        deleteBtn.offsetParent.parentNode.remove();
                    });
                }
            }
            Xhr.send( data );

        });
    }
}