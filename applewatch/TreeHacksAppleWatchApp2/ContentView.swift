//
//  ContentView.swift
//  TreeHacksAppleWatchApp2
//
//  Created by Charlotte Chang on 2/15/25.
//

import SwiftUI
import HealthKit


struct ContentView: View {
    @StateObject private var heartRateManager = HeartRateManager()
    
    var body: some View {
        NavigationView {
            List(heartRateManager.heartRateReadings) { reading in
                VStack(alignment: .leading) {
                    Text("Heart Rate: \(Int(reading.heartRate)) BPM")
                    Text("Time: \(reading.timestamp, style: .time)")
                }
            }
            .navigationTitle("Heart Rate Readings")
        }
        .onAppear {
            heartRateManager.requestAuthorization()
        }
    }
}

class HeartRateManager: ObservableObject {
    private var healthStore = HKHealthStore()
    @Published var heartRateReadings: [HeartRateReading] = []
    private var observerQuery: HKObserverQuery?
    private var dataFetchTimer: Timer?
    private var dataClearTimer: Timer?
    //private let db = Firestore.firestore()
    
    func requestAuthorization() {
        let heartRateType = HKQuantityType.quantityType(forIdentifier: .heartRate)!
        healthStore.requestAuthorization(toShare: [], read: [heartRateType]) { success, error in
            if success {
                DispatchQueue.main.async {
                    self.startHeartRateMonitoring()
                }
            }
        }
    }
    
    func startHeartRateMonitoring() {
        let heartRateType = HKQuantityType.quantityType(forIdentifier: .heartRate)!
        
        observerQuery = HKObserverQuery(sampleType: heartRateType, predicate: nil) { [weak self] query, completionHandler, error in
            if error == nil {
                self?.fetchLatestHeartRate()
            }
            completionHandler()
        }
        
        if let observerQuery = observerQuery {
            healthStore.execute(observerQuery)
        }
        
        healthStore.enableBackgroundDelivery(for: heartRateType, frequency: .immediate) { success, error in
            if success {
                print("Background delivery enabled")
            } else if let error = error {
                print("Error enabling background delivery: \(error.localizedDescription)")
            }
        }
        
        dataFetchTimer = Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.fetchLatestHeartRate()
        }
        
        dataClearTimer = Timer.scheduledTimer(withTimeInterval: 600, repeats: true) { [weak self] _ in
            self?.clearHeartRateData()
        }
    }
    
    private func fetchLatestHeartRate() {
        let heartRateType = HKQuantityType.quantityType(forIdentifier: .heartRate)!
        let predicate = HKQuery.predicateForSamples(withStart: Date().addingTimeInterval(-60), end: nil, options: .strictEndDate)
        
        let query = HKStatisticsQuery(quantityType: heartRateType, quantitySamplePredicate: predicate, options: .mostRecent) { [weak self] _, statistics, error in
            guard let statistics = statistics, let quantity = statistics.mostRecentQuantity() else {
                return
            }
            
            let heartRate = quantity.doubleValue(for: HKUnit.count().unitDivided(by: .minute()))
            let timestamp = statistics.startDate
            let reading = HeartRateReading(heartRate: heartRate, timestamp: timestamp)
            
            DispatchQueue.main.async {
                self?.heartRateReadings.append(reading)
                if self?.heartRateReadings.count ?? 0 > 20 {
                    self?.heartRateReadings.removeFirst()
                }
                /*self?.sendDataToFirestore(heartRate: heartRate, timestamp: timestamp)
            }*/
        }
        
        healthStore.execute(query)
    }
    
    /*private func sendDataToFirestore(heartRate: Double, timestamp: Date) {
        let data: [String: Any] = [
            "heartRate": heartRate,
            "timestamp": timestamp
        ]
        
        db.collection("heartRates").addDocument(data: data) { error in
            if let error = error {
                print("Error sending data to Firestore: \(error.localizedDescription)")
            } else {
                print("Heart rate data sent to Firestore successfully: \(heartRate) BPM at \(timestamp)")
            }
        }
    }*/
    
    private func clearHeartRateData() {
        DispatchQueue.main.async {
            if let lastReading = self.heartRateReadings.last {
                self.heartRateReadings = [lastReading]
            } else {
                self.heartRateReadings.removeAll()
            }
            print("Heart rate data cleared, keeping last reading if available")
        }
    }
    
    deinit {
        dataFetchTimer?.invalidate()
        dataClearTimer?.invalidate()
        if let observerQuery = observerQuery {
            healthStore.stop(observerQuery)
        }
    }
}

struct HeartRateReading: Identifiable {
    let id = UUID()
    let heartRate: Double
    let timestamp: Date
}


#Preview {
    ContentView()
}
