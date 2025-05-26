// swift-tools-version:5.7
import PackageDescription

let package = Package(
  name: "script_analyzer_bot",
  platforms: [
    .macOS(.v13)
  ],
  products: [
    .executable(name: "ScriptAnalyzerBot", targets: ["App"])
  ],
  dependencies: [
    // Vapor web framework for API and server-side Swift
    .package(url: "https://github.com/vapor/vapor.git", from: "4.0.0"),
    
    // Vapor Queues for async task handling (e.g., background AI jobs)
    .package(url: "https://github.com/vapor/queues.git", from: "1.0.0"),
    
    // Google Generative AI SDK (local path assumed; update if remote)
    .package(name: "GoogleGenerativeAI", path: "../GoogleGenerativeAI")
  ],
  targets: [
    .executableTarget(
      name: "App",
      dependencies: [
        .product(name: "Vapor", package: "vapor"),
        .product(name: "Queues", package: "queues"),
        "GoogleGenerativeAI"
      ],
      path: "Sources"
    )
  ]
)
