//
//  HeartRateReading.swift
//  TreeHacksAppleWatchApp2
//
//  Created by Charlotte Chang on 2/16/25.
//

import Foundation

struct HeartRateReading: Identifiable {
    let id = UUID()
    let heartRate: Double
    let timestamp: Date
}
