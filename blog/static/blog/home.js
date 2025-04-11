/***<!-- filepath: d:\Desktop\fotoblog\fotoblog\blog\home.js->***/

document.addEventListener("DOMContentLoaded", function () {
  // ==== Filtres et vues ====
  const filterBtn = document.querySelector(".jsFilter");
  if (filterBtn) {
    filterBtn.addEventListener("click", function () {
      document.querySelector(".filter-menu").classList.toggle("active");
    });
  }

  const gridBtn = document.querySelector(".grid");
  const listBtn = document.querySelector(".list");
  const wrapper = document.querySelector(".products-area-wrapper");

  if (gridBtn && listBtn && wrapper) {
    gridBtn.addEventListener("click", function () {
      listBtn.classList.remove("active");
      gridBtn.classList.add("active");
      wrapper.classList.add("gridView");
      wrapper.classList.remove("tableView");
    });

    listBtn.addEventListener("click", function () {
      listBtn.classList.add("active");
      gridBtn.classList.remove("active");
      wrapper.classList.remove("gridView");
      wrapper.classList.add("tableView");
    });
  }

  // ==== Thème clair/sombre ====
  const savedTheme = localStorage.getItem("theme");
  if (savedTheme === "light") {
    document.documentElement.classList.add("light");
    const modeBtn = document.querySelector(".mode-switch");
    if (modeBtn) {
      modeBtn.classList.add("active");
    }
  }

  const modeSwitch = document.querySelector(".mode-switch");
  if (modeSwitch) {
    modeSwitch.addEventListener("click", function () {
      document.documentElement.classList.toggle("light");
      modeSwitch.classList.toggle("active");

      const isLight = document.documentElement.classList.contains("light");
      localStorage.setItem("theme", isLight ? "light" : "dark");
    });
  }

  // ==== Modale et notification pour ADD & DELETE ====
  let selectedJanteId = null;
  let selectedButton = null;

  const modal = document.getElementById("confirmation-modal");
  const btnOui = document.getElementById("confirm-oui");
  const btnNon = document.getElementById("confirm-non");
  const modalMessage = document.getElementById("modal-message"); // 💡 Pour modifier le texte

  // Création notification dynamique
  let notifier = document.getElementById("notification-success");
  if (!notifier) {
    notifier = document.createElement("div");
    notifier.id = "notification-success";
    notifier.textContent = "";
    Object.assign(notifier.style, {
      position: "fixed",
      bottom: "30px",
      right: "30px",
      background: "#28a745",
      color: "#fff",
      padding: "12px 20px",
      borderRadius: "8px",
      display: "none",
      boxShadow: "0 2px 10px rgba(0,0,0,0.2)",
      zIndex: "10000",
      transition: "opacity 0.5s ease",
      opacity: "0"
    });
    document.body.appendChild(notifier);
  }

  // Fonctions appelées par les boutons HTML
  window.confirmerDepose = function(janteId, buttonElement) {
    const row = buttonElement.closest('tr');
    const serialNumber = row.cells[2].textContent; // 3ème colonne = Serial Number
    
    showCustomModal(
        `Voulez-vous ajouter une dépose à la jante ${serialNumber} ?`,
        (confirmed) => {
            if (confirmed) {
                const url = `/ajouter-depose/${janteId}/`;
                fetch(url, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCookie("csrftoken") },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification("Dépose ajoutée avec succès !");
                        // Mise à jour des 3 colonnes
                        row.cells[4].textContent = data.nombre_de_deposes;
                        row.cells[5].textContent = data.dernier_ndi;
                        row.cells[6].textContent = data.prochain_ndi;
                    } else {
                        showNotification(data.message || "Erreur lors de l'ajout", 'error');
                    }
                });
            }
        }
    );
};

  window.confirmerRetrait = function(janteId, buttonElement) {
    const row = buttonElement.closest('tr');
    const serialNumber = row.cells[2].textContent; // 3ème colonne = Serial Number
    
    showCustomModal(
        `Voulez-vous retirer une dépose à la jante ${serialNumber} ?`,
        (confirmed) => {
            if (confirmed) {
                const url = `/retirer-depose/${janteId}/`;
                fetch(url, {
                    method: "POST",
                    headers: { "X-CSRFToken": getCookie("csrftoken") },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification("Dépose retirée avec succès !");
                        // Mise à jour des 3 colonnes
                        row.cells[4].textContent = data.nombre_de_deposes;
                        row.cells[5].textContent = data.dernier_ndi;
                        row.cells[6].textContent = data.prochain_ndi;
                    } else {
                        showNotification(data.message || "Erreur lors du retrait", 'error');
                    }
                });
            }
        }
    );
};

  // NON → fermer la modale
  if (btnNon) {
    btnNon.addEventListener("click", function () {
      modal.style.display = "none";
    });
  }

  // OUI → effectuer l'action
  if (btnOui) {
    btnOui.addEventListener("click", function () {
        const action = modal.dataset.action;
        const url =
            action === "add"
                ? `/ajouter-depose/${selectedJanteId}/`
                : `/retirer-depose/${selectedJanteId}/`;

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    showNotification(data.message || "Action réussie !");
                    if (action === "add") {
                        selectedButton.closest("tr").querySelector(
                            "td:nth-child(5)"
                        ).textContent = data.nombre_de_deposes;
                    }
                } else {
                    alert(data.message || "Une erreur est survenue.");
                }
                modal.style.display = "none";
            })
            .catch((error) => {
                console.error("Erreur :", error);
                alert("Une erreur est survenue.");
                modal.style.display = "none";
            });
    });
  }

  // Afficher une notification
  function showNotification(message) {
    notifier.textContent = message;
    notifier.style.display = "block";
    setTimeout(() => {
      notifier.style.opacity = "1";
    }, 10);
    setTimeout(() => {
      notifier.style.opacity = "0";
      setTimeout(() => {
        notifier.style.display = "none";
      }, 500);
    }, 3000);
  }

  // CSRF helper
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // ==== Barre de recherche ====
  const searchBar = document.getElementById("search-bar");
  const table = document.getElementById("products-table");
  const rows = table.querySelectorAll("tbody tr");

  if (searchBar) {
    searchBar.addEventListener("input", function () {
      const searchValue = searchBar.value.toLowerCase();

      rows.forEach((row) => {
        const serialNumberCell = row.querySelector("td:nth-child(3)"); // 3ème colonne pour SERIAL NUMBER
        if (serialNumberCell) {
          const serialNumber = serialNumberCell.textContent.toLowerCase();
          if (serialNumber.includes(searchValue) || searchValue === "") {
            row.style.display = ""; // Affiche la ligne si elle correspond ou si la barre est vide
          } else {
            row.style.display = "none"; // Cache la ligne si elle ne correspond pas
          }
        }
      });
    });
  }

  // ==== Filtre par catégorie ====
  const categoryFilter = document.getElementById("category-filter");
  if (categoryFilter) {
    categoryFilter.addEventListener("change", function () {
      const selectedCategory = categoryFilter.value.toLowerCase();

      rows.forEach((row) => {
        const categoryCell = row.querySelector("td:nth-child(2)"); // 2ème colonne pour CATEGORY
        if (categoryCell) {
          const category = categoryCell.textContent.toLowerCase();
          if (selectedCategory === "all" || category === selectedCategory) {
            row.style.display = ""; // Affiche la ligne si elle correspond ou si "All Categories" est sélectionné
          } else {
            row.style.display = "none"; // Cache la ligne si elle ne correspond pas
          }
        }
      });
    });
  }

  // ==== Notifications ====
  const notificationsLink = document.querySelector('a[href="/NOTIFICATIONS/"]');

  if (notificationsLink) {
    notificationsLink.addEventListener("click", function () {
      fetch("/mark-notifications-as-read/", {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
      })
        .then((res) => {
          if (!res.ok) throw new Error("Erreur HTTP");
          return res.json();
        })
        .then((data) => {
          if (data.success) {
            const dot = document.querySelector(".notification-dot");
            if (dot) dot.style.display = "none"; // Cache le point rouge
          }
        })
        .catch((err) => {
          console.error("Erreur : ", err);
        });
    });
  }
});

function updateObs(textarea) {
  const janteId = textarea.dataset.janteId;
  const obsValue = textarea.value;

  fetch(`/update-obs/${janteId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: `obs=${encodeURIComponent(obsValue)}`,
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        console.log("Observation mise à jour :", data.obs);
      } else {
        alert("Erreur : " + data.message);
      }
    })
    .catch((error) => {
      console.error("Erreur lors de la mise à jour de l'observation :", error);
    });
}

// Fonction pour récupérer le token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function updateNotificationDot() {
  console.log("Vérification des notifications non lues...");
  fetch("/check-unread-notifications/", {
    method: "GET",
    headers: {
      "X-CSRFToken": getCookie("csrftoken"),
    },
  })
    .then((res) => {
      if (!res.ok) throw new Error("Erreur HTTP");
      return res.json();
    })
    .then((data) => {
      console.log("Réponse du serveur :", data);
      const dot = document.querySelector(".notification-dot");
      if (data.has_unread_notifications) {
        if (dot) {
          dot.style.display = "inline-block"; // Affiche le point rouge
          console.log("Point rouge affiché.");
        }
      } else {
        if (dot) {
          dot.style.display = "none"; // Cache le point rouge
          console.log("Point rouge caché.");
        }
      }
    })
    .catch((err) => {
      console.error("Erreur lors de la mise à jour des notifications :", err);
    });
}

setInterval(updateNotificationDot, 5000); // Vérifie toutes les 5 secondes

// Nouvelle fonction pour gérer les actions ADD/DELETE
function handleAction(janteId, actionType) {
  const actionMap = {
      'add': {
          url: `/ajouter-depose/${janteId}/`,
          confirmMsg: `Voulez-vous ajouter une dépose à la jante ${janteId} ?`,
          successMsg: 'Dépose ajoutée avec succès',
          errorMsg: 'Erreur lors de l\'ajout'
      },
      'delete': {
          url: `/retirer-depose/${janteId}/`,
          confirmMsg: `Voulez-vous retirer une dépose de la jante ${janteId} ?`,
          successMsg: 'Dépose retirée avec succès',
          errorMsg: 'Erreur lors du retrait'
      }
  };

  const action = actionMap[actionType];
  
  if (confirm(action.confirmMsg)) {
      fetch(action.url, {
          method: 'POST',
          headers: {
              'X-CSRFToken': getCookie('csrftoken'),
              'Content-Type': 'application/json'
          }
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              updateJanteRow(janteId, data);
              showNotification(action.successMsg, 'success');
          } else {
              showNotification(data.message || action.errorMsg, 'error');
          }
      })
      .catch(error => {
          showNotification('Erreur réseau: ' + error.message, 'error');
      });
  }
}

// Met à jour uniquement la ligne concernée
function updateJanteRow(janteId, data) {
  const row = document.querySelector(`tr[data-jante-id="${janteId}"]`);
  if (row) {
      // Met à jour uniquement si les valeurs existent dans la réponse
      if (data.nombre_de_deposes !== undefined) {
          row.cells[4].textContent = data.nombre_de_deposes;
      }
      if (data.dernier_ndi !== undefined) {
          row.cells[5].textContent = data.dernier_ndi;
      }
      if (data.prochain_ndi !== undefined) {
          row.cells[6].textContent = data.prochain_ndi;
      }
  }
}

// Affiche une notification (utilise le système existant)
function showNotification(message, type) {
  const notifier = document.getElementById('notification-success');
  if (notifier) {
      notifier.textContent = message;
      notifier.style.background = type === 'success' ? '#28a745' : '#dc3545';
      notifier.style.display = 'block';
      notifier.style.opacity = '1';
      
      setTimeout(() => {
          notifier.style.opacity = '0';
          setTimeout(() => {
              notifier.style.display = 'none';
          }, 500);
      }, 3000);
  } else {
      alert(message); // Fallback si le système de notification n'existe pas
  }
}

// Fonction pour afficher une modale personnalisée
function showCustomModal(message, callback) {
    // Crée la modale si elle n'existe pas
    let modal = document.getElementById('custom-confirm-modal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'custom-confirm-modal';
        modal.style.display = 'none';
        modal.style.position = 'fixed';
        modal.style.top = '0';
        modal.style.left = '0';
        modal.style.width = '100%';
        modal.style.height = '100%';
        modal.style.backgroundColor = 'rgba(0,0,0,0.5)';
        modal.style.zIndex = '1000';
        modal.style.justifyContent = 'center';
        modal.style.alignItems = 'center';
        
        modal.innerHTML = `
            <div style="background: white; padding: 20px; border-radius: 8px; max-width: 400px; text-align: center;">
                <p id="custom-modal-message" style="margin-bottom: 20px; font-size: 1.1rem;"></p>
                <div style="display: flex; justify-content: center; gap: 10px;">
                    <button id="custom-modal-yes" style="padding: 8px 20px; background: #2869ff; color: white; border: none; border-radius: 4px; cursor: pointer;">OUI</button>
                    <button id="custom-modal-no" style="padding: 8px 20px; background: #f0f0f0; border: none; border-radius: 4px; cursor: pointer;">NON</button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    // Configure le message
    document.getElementById('custom-modal-message').textContent = message;
    
    // Gestion des boutons
    const yesBtn = document.getElementById('custom-modal-yes');
    const noBtn = document.getElementById('custom-modal-no');

    // Nettoyage des anciens événements
    yesBtn.replaceWith(yesBtn.cloneNode(true));
    noBtn.replaceWith(noBtn.cloneNode(true));

    // Ajout des nouveaux événements
    document.getElementById('custom-modal-yes').onclick = function() {
        modal.style.display = 'none';
        callback(true);
    };
    document.getElementById('custom-modal-no').onclick = function() {
        modal.style.display = 'none';
        callback(false);
    };

    // Affiche la modale
    modal.style.display = 'flex';
}
// Fonctions simplifiées et garanties
function handleAdd(serialNumber, janteId, button) {
  showConfirmModal(
      `Voulez-vous ajouter une dépose à la jante ${serialNumber} ?`,
      () => performAction(janteId, 'add', button)
  );
}

function handleDelete(serialNumber, janteId, button) {
  showConfirmModal(
      `Voulez-vous retirer une dépose à la jante ${serialNumber} ?`,
      () => performAction(janteId, 'delete', button)
  );
}

function showConfirmModal(message, callback) {
    const modal = document.createElement('div');
    modal.style = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;
    
    modal.innerHTML = `
        <div style="
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 400px;
            text-align: center;
        ">
            <p style="margin-bottom: 20px; color: black; font-size: 1.2rem;">${message}</p>
            <div>
                <button id="confirm-yes" style="
                    padding: 8px 20px;
                    margin-right: 10px;
                    background: #28a745; /* Vert pour OUI */
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                ">OUI</button>
                <button id="confirm-no" style="
                    padding: 8px 20px;
                    background: #007bff; /* Bleu pour NON */
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                ">NON</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    document.getElementById('confirm-yes').onclick = () => {
        document.body.removeChild(modal);
        callback(true);
    };
    
    document.getElementById('confirm-no').onclick = () => {
        document.body.removeChild(modal);
        callback(false);
    };
}

function performAction(janteId, action, button) {
  const url = action === 'add' 
      ? `/ajouter-depose/${janteId}/` 
      : `/retirer-depose/${janteId}/`;
  
  fetch(url, {
      method: 'POST',
      headers: {
          'X-CSRFToken': getCookie('csrftoken'),
      },
  })
  .then(response => response.json())
  .then(data => {
      if (data.success) {
          const row = button.closest('tr');
          row.cells[4].textContent = data.nombre_de_deposes;
          row.cells[5].textContent = data.dernier_ndi;
          row.cells[6].textContent = data.prochain_ndi;
          showFeedback('Action réussie !', 'success');
      } else {
          showFeedback(data.message || 'Erreur', 'error');
      }
  })
  .catch(error => {
      showFeedback('Erreur réseau', 'error');
      console.error(error);
  });
}

function showFeedback(message, type) {
  const feedback = document.createElement('div');
  feedback.style = `
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 12px 20px;
      background: ${type === 'success' ? '#28a745' : '#dc3545'}; /* Vert pour succès, rouge pour erreur */
      color: white; /* Couleur du texte */
      font-size: 1rem; /* Taille du texte */
      font-weight: bold; /* Texte en gras */
      border-radius: 4px;
      z-index: 1000;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2); /* Ombre pour un meilleur contraste */
  `;
  feedback.textContent = message;
  document.body.appendChild(feedback);
  
  setTimeout(() => {
      feedback.remove();
  }, 3000);
}

function showConfirmModal(message, callback) {
    const modal = document.createElement('div');
    modal.style = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 1000;
    `;
    
    modal.innerHTML = `
        <div style="
            background: white;
            padding: 20px;
            border-radius: 8px;
            width: 80%;
            max-width: 400px;
            text-align: center;
        ">
            <p style="margin-bottom: 20px; color: black; font-size: 1.2rem;">${message}</p>
            <div>
                <button id="confirm-yes" style="
                    padding: 8px 20px;
                    margin-right: 10px;
                    background: #28a745; /* Vert pour OUI */
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                ">OUI</button>
                <button id="confirm-no" style="
                    padding: 8px 20px;
                    background: #007bff; /* Bleu pour NON */
                    color: white;
                    border: none;
                    border-radius: 4px;
                    cursor: pointer;
                ">NON</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    
    // Action pour le bouton OUI
    document.getElementById('confirm-yes').onclick = () => {
        document.body.removeChild(modal);
        callback(true); // Exécute l'action si OUI est cliqué
    };
    
    // Action pour le bouton NON
    document.getElementById('confirm-no').onclick = () => {
        document.body.removeChild(modal);
        callback(false); // Ne fait rien si NON est cliqué
    };
}

function handleAdd(serialNumber, janteId, button) {
    showConfirmModal(
        `Voulez-vous ajouter une dépose à la jante ${serialNumber} ?`,
        (confirmed) => {
            if (confirmed) {
                performAction(janteId, 'add', button); // Exécute l'action uniquement si OUI est cliqué
            }
        }
    );
}

function handleDelete(serialNumber, janteId, button) {
    showConfirmModal(
        `Voulez-vous retirer une dépose à la jante ${serialNumber} ?`,
        (confirmed) => {
            if (confirmed) {
                performAction(janteId, 'delete', button); // Exécute l'action uniquement si OUI est cliqué
            }
        }
    );
}