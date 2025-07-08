const foodItem = [
  { id: 1, name: "burger", time: 5 },
  { id: 2, name: "pizza", time: 7 },
  { id: 3, name: "pasta", time: 8 },
  { id: 4, name: "sandwich", time: 4 },
  { id: 5, name: "sushi", time: 6 },
];
const orderStorage = [];

// Submit order to backend and start animation
function submitOrder() {
  if (orderStorage.length > 0) {
    document.getElementById("submitBtn").disabled = true;
    fetch("/order", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(orderStorage),
    })
      .then((response) => response.json())
      .then((responseData) => {
        if (responseData.details) {
          startAnimations(responseData.details, 0);
        }
        orderStorage.length = 0;
        updateOrderList();
      })
      .catch((error) => {
        alert("Error processing order!");
        document.getElementById("submitBtn").disabled = false;
        console.error("Error:", error);
      });
  } else {
    alert("No orders to submit.");
  }
}

// Add order to the orderStorage and update the modal instantly
function addOder(tableNumber, foodItemId) {
  const order = orderStorage.find((order) => order.tableNumber === tableNumber);
  if (order) {
    const food = order.foodItems.find((item) => item.id === Number(foodItemId));
    if (food) {
      food.quantity++;
    } else {
      order.foodItems.push({ id: Number(foodItemId), quantity: 1 });
    }
  } else {
    orderStorage.push({
      tableNumber,
      foodItems: [{ id: Number(foodItemId), quantity: 1 }],
    });
  }
  showOrderModal(tableNumber);
  updateOrderList();
}

// Live-updating order list in the modal and outside (optional)
function updateOrderList() {
  const orderList = document.getElementById("orderList");
  if (!orderList) return;
  orderList.innerHTML = "";
  orderStorage.forEach((order) => {
    order.foodItems.forEach((item) => {
      const food = foodItem.find((food) => food.id === Number(item.id));
      const li = document.createElement("li");
      li.className = "list-group-item";
      li.textContent = `${food.name} x ${item.quantity} - ${order.tableNumber}`;
      orderList.appendChild(li);
    });
  });
}

// Render chessboard grid and attach click events to tables
document.addEventListener("DOMContentLoaded", function () {
  const chessboard = document.querySelector(".chessboard");
  const rows = 9, cols = 9;
  let tableNumber = 1;
  for (let i = 0; i < rows; i++) {
    for (let j = 0; j < cols; j++) {
      const square = document.createElement("div");
      square.classList.add("square");
      square.dataset.row = i;
      square.dataset.col = j;
      if (i === 0 && (j === 0 || j === 5 || j === 8)) {
        square.classList.add("food");
        square.id = `t${tableNumber}`;
        tableNumber++;
      } else if (i === 2 && (j === 0 || j === 8)) {
        square.classList.add("food");
        square.id = `t${tableNumber}`;
        tableNumber++;
      } else if (i === 5 && j === 0) {
        square.classList.add("food");
        square.id = `t${tableNumber}`;
        tableNumber++;
      } else if (i === 6 && j === 7) {
        square.classList.add("food");
        square.id = `t${tableNumber}`;
        tableNumber++;
      } else if (i === 8 && (j === 0 || j === 2 || j === 6)) {
        square.classList.add("food");
        square.id = `t${tableNumber}`;
        tableNumber++;
      } else if (i === 4 && j === 4) {
        square.classList.add("kitchen");
        square.id = "kit";
      } else if (i % 2 === j % 2) {
        square.classList.add("white");
      } else {
        square.classList.add("black");
      }
      // Walls
      if (i === 1 || i === 2 || i == 3 || i == 4 || i >= 6) {
        if (i == 1 && (j == 4 || j == 5)) square.classList.add("wall");
        if (i == 2 && j == 2) square.classList.add("wall");
        if (i == 3 && (j <= 3 || j == 6 || j == 7)) square.classList.add("wall");
        if (i == 4 && j <= 1) square.classList.add("wall");
        if (i == 6 && j == 6) square.classList.add("wall");
        if (i == 7 && j >= 6) square.classList.add("wall");
        if (i == 8 && (j == 1 || j == 3 || j == 4 || j >= 7)) square.classList.add("wall");
      }
      chessboard.appendChild(square);
    }
  }
  document.querySelectorAll(".food").forEach((square) => {
    square.addEventListener("click", () => {
      showOrderModal(square.id);
    });
  });
});

// Modal popup for food selection (updates live with every selection)
function showOrderModal(tableNumber) {
  // Remove any existing modal
  document.querySelectorAll('.modal').forEach(m => m.parentNode.removeChild(m));
  // Remove any lingering modal-backdrop (fixes screen stuck bug)
  document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());

  const order = orderStorage.find((order) => order.tableNumber === tableNumber);
  let orderListHTML = '';
  if (order && order.foodItems.length > 0) {
    orderListHTML = '<ul class="list-group">';
    order.foodItems.forEach((item) => {
      const food = foodItem.find((food) => food.id === Number(item.id));
      orderListHTML += `<li class="list-group-item">${food.name} x ${item.quantity}</li>`;
    });
    orderListHTML += '</ul>';
  } else {
    orderListHTML = '<div class="text-muted">No orders yet.</div>';
  }
  const modal = document.createElement("div");
  modal.classList.add("modal", "fade");
  modal.tabIndex = -1;
  modal.innerHTML = `
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Table ${tableNumber}</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body text-center">
          ${foodItem.map(item =>
            `<span class="badge bg-primary mx-1 selectBadge p-3"
            style="cursor:pointer; font-size:1.2em;"
            onclick="addOder('${tableNumber}','${item.id}')">${item.name}</span>`
          ).join("")}
          <hr>
          <h6>Order List</h6>
          ${orderListHTML}
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        </div>
      </div>
    </div>`;
  document.body.appendChild(modal);

  const modalInstance = new bootstrap.Modal(modal);
  modalInstance.show();

  // Remove modal and modal-backdrop from DOM after close
  modal.addEventListener('hidden.bs.modal', () => {
    document.body.removeChild(modal);
    document.querySelectorAll('.modal-backdrop').forEach(b => b.remove());
  });
}

// Animation handler (robot waiter movement)
function startAnimations(data, index) {
  document.querySelectorAll('.active-waiter').forEach(el => el.classList.remove('active-waiter'));
  if (index >= data.length) {
    document.getElementById("submitBtn").disabled = false;
    return;
  }
  const path = data[index].path;
  const reversePath = [...path].reverse();
  startAnimation(path, 350, () => {
    startAnimation(reversePath, 350, () => {
      startAnimations(data, index + 1);
    });
  });
};
const startAnimation = (path, timeDelay = 800, callback) => {
  let i = 0;
  const interval = setInterval(() => {
    const square = document.querySelector(
      `.square[data-row="${path[i].row}"][data-col="${path[i].col}"]`
    );
    if (square) square.classList.add("active-waiter");
    setTimeout(() => {
      if (square) square.classList.remove("active-waiter");
    }, timeDelay);
    i++;
    if (i === path.length) {
      clearInterval(interval);
      callback();
    }
  }, timeDelay);
};
