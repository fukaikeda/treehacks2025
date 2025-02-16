//
//  ContentView.swift
//  TreeHacksAppleWatchApp2 Watch App
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

#Preview {
    ContentView()
}
