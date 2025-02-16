//
//  TreeHacksAppleWatchApp2App.swift
//  TreeHacksAppleWatchApp2
//
//  Created by Charlotte Chang on 2/15/25.
//

import SwiftUI
import FirebaseCore

@main
struct TreeHacksAppleWatchApp2App: App {
    init() {
        FirebaseApp.configure()
    }
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}

