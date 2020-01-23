var goalValue = document.getElementsByClassName("goal"),
    reachedValue = document.getElementsByClassName("reached"),
    progressBar = document.getElementsByClassName("progress-bar"),
    donationAmountBtn = document.getElementsByClassName("donation-amount-label"),
    maxValueToDonate = document.getElementsByClassName("max-donation-value"),
    commentBtn = document.querySelector(".comment-btn"),
    commentField = document.querySelector(".comment-field");

// Set up max donation value
for(let i = 0; i < maxValueToDonate.length; i++){
    maxValueToDonate[i].childNodes[1].value = parseInt(goalValue[i].textContent) - parseInt(reachedValue[i].textContent);
    maxValueToDonate[i].childNodes[3].textContent = parseInt(goalValue[i].textContent) - parseInt(reachedValue[i].textContent);
}


// Progress bar fill
for(var i = 0; i < progressBar.length; i++){
    var progressBarResult = parseInt(reachedValue[i].textContent) / parseInt(goalValue[i].textContent) * 100;
    progressBar[i].style.width = progressBarResult + "%";
}

// Form image upload for user profile photo
if(document.getElementsByClassName("profile-photo-btn")[0]) {
    document.getElementsByClassName("profile-photo-btn")[0].addEventListener("click", function(){
        document.getElementsByClassName("profile-photo-input")[0].click();
    });
}

// Form image upload for waiting challenge photo
if(document.getElementsByClassName("waiting-file-btn")[0]) {
    document.getElementsByClassName("waiting-file-btn")[0].addEventListener("click", function(){
        document.getElementsByClassName("waiting-file-input")[0].click();
    });
}

// change donation button color on click
for(let i = 0; i < donationAmountBtn.length; i++){
    donationAmountBtn[i].addEventListener('click', function(){
        let active = document.getElementsByClassName("active-donation")[0];
        if(active){
            if(active.childNodes[1]){
                active.childNodes[1].checked = false;
            }
            active.classList.remove("active-donation");
        };
        if(this.childNodes[1]){
            this.childNodes[1].checked = true;
        }
        this.classList.add("active-donation");
    });
}

if(commentBtn){
    commentBtn.addEventListener('click', function(){
        commentField.classList.toggle('opacity-zero');
        if(commentField.classList.contains('d-none')){
            commentField.classList.remove('d-none');
        }
        commentField.addEventListener('transitionend', function(){
            commentField.classList.add('d-none');
        })
        commentBtn.classList.toggle('text-warning');
    });
}
