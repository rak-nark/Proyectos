package main

import (
	"fmt"
	"time"

	"github.com/shirou/gopsutil/v3/cpu"
	"github.com/shirou/gopsutil/v3/disk"
	"github.com/shirou/gopsutil/v3/mem"
)

func main() {
	for {
		printStats()
		time.Sleep(2 * time.Second)
	}
}

func printStats() {
	fmt.Print("\033[H\033[2J") // Limpia la terminal

	// CPU
	percent, _ := cpu.Percent(0, false)
	fmt.Printf("🧠 CPU Usage: %.2f%%\n", percent[0])

	// RAM
	vmStat, _ := mem.VirtualMemory()
	fmt.Printf("📦 RAM Usage: %.2f%% (%v / %v)\n", vmStat.UsedPercent, byteToMB(vmStat.Used), byteToMB(vmStat.Total))

	// Disk
	diskStat, _ := disk.Usage("/")
	fmt.Printf("💾 Disk Usage: %.2f%% (%v / %v)\n", diskStat.UsedPercent, byteToGB(diskStat.Used), byteToGB(diskStat.Total))
}

func byteToMB(b uint64) string {
	return fmt.Sprintf("%.2f MB", float64(b)/1024/1024)
}

func byteToGB(b uint64) string {
	return fmt.Sprintf("%.2f GB", float64(b)/1024/1024/1024)
}
