const deleteButton = document.querySelectorAll("table td .bi-trash");
const modal = document.getElementById("modal-delete");

deleteButton.forEach((button) => {
  button.addEventListener("click", (e) => {
    const formDelete = modal.querySelector("form");

    if (formDelete) {
      formDelete.setAttribute("action", e.target.dataset.url);
    }
  });
});
