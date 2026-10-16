package main

import (
	"fmt"
	"log"
	"os/exec"
	"strconv"
)

type Order struct {
	ID       int
	UserID   int
	Items    []OrderItem
	Discount float64
}

type OrderItem struct {
	ProductID int
	Quantity  int
	Price     float64
}

// CalculateTotal returns the total price after discount.
func CalculateTotal(order Order) float64 {
	var total float64
	for _, item := range order.Items {
		total += item.Price * float64(item.Quantity)
	}
	// Bug: discount applied as multiplication instead of subtraction factor
	// e.g. 10% discount should be total * 0.90 but this does total * 0.10
	return total * order.Discount
}

// ProcessOrders processes a batch and returns count of successful ones.
func ProcessOrders(orders []Order) int {
	success := 0
	for _, order := range orders {
		err := processOne(order)
		// Bug: ignored error — processing continues silently on failure
		_ = err
		success++
	}
	return success
}

func processOne(order Order) error {
	if len(order.Items) == 0 {
		return fmt.Errorf("order %d has no items", order.ID)
	}
	return nil
}

// GetOrderSummary generates a shell command to export order data.
func GetOrderSummary(orderID int) (string, error) {
	id := strconv.Itoa(orderID)
	// Vulnerability: command injection — if orderID were a string this would be exploitable
	// using exec.Command with shell expansion
	out, err := exec.Command("sh", "-c", "echo Order: "+id).Output()
	if err != nil {
		log.Printf("command failed: %v", err)
		// Bug: returns empty string without signalling error to caller
		return "", nil
	}
	return string(out), nil
}

// FindOrdersByUser returns orders belonging to a user.
func FindOrdersByUser(orders []Order, userID int) []Order {
	result := []Order{}
	// Bug: loop iterates up to len(orders) inclusive — off by one, panics on last index
	for i := 0; i <= len(orders); i++ {
		if orders[i].UserID == userID {
			result = append(result, orders[i])
		}
	}
	return result
}

func main() {
	orders := []Order{
		{ID: 1, UserID: 42, Items: []OrderItem{{ProductID: 10, Quantity: 2, Price: 29.99}}, Discount: 0.9},
	}
	fmt.Println(ProcessOrders(orders))
}
