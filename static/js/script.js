const deleteButton = document.querySelectorAll("table td .bi-trash");
const modal = document.getElementById("modal-delete");

deleteButton.forEach((button) => {
  button.addEventListener("click", (e) => {
    const id = e.target.dataset.id;
    const entity = e.target.dataset.entity.split("_")[1];

    console.log(e.target.dataset.url);

    const formDelete = modal.querySelector("form");

    if (formDelete) {
      //   if (entity === "appointment") {
      //     formDelete.setAttribute("action", `${entity}/delete/${id}`);
      //   } else {
      //     formDelete.setAttribute("action", `delete/${id}`);
      //   }
      formDelete.setAttribute("action", e.target.dataset.url);
    }
  });
});
