const { MongoClient } = require("mongodb");

const uri = "mongodb+srv://ctchang:lJ8XJpRv0p9EqM7b@treehacks25.8m1qt.mongodb.net/?retryWrites=true&w=majority&appName=TreeHacks25";
const client = new MongoClient(uri);

async function run() {
    try {
        await client.connect();
        console.log("Connected to MongoDB");

        const db = client.db("TreeHacks25");
        const collection = db.collection("activity");

        // Fetch all heart rate data
        const heartRateData = await collection.find(
            {}, 
            { projection: { "heart_rate_data.detailed.hr_samples": 1, _id: 0 } }
        ).toArray();

        // Print all data in a readable format
        console.log(JSON.stringify(heartRateData, null, 2)); // Pretty-print with indentation
    } finally {
        await client.close();
    }
}

run().catch(console.dir);

