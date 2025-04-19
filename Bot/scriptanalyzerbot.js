const { ActivityHandler } = require('botbuilder');
const fs = require('fs');
const path = require('path');

class ScriptAnalyzerBot extends ActivityHandler {
    constructor() {
        super();

        this.onMessage(async (context, next) => {
            const text = context.activity.text.toLowerCase();

            if (text.includes('analyze my scripts')) {
                const directoryPath = './scripts';
                const result = this.analyzeDirectory(directoryPath);
                await context.sendActivity(result);
            } else {
                await context.sendActivity("🧠 Say 'analyze my scripts' and make sure your JS files are in the `/scripts` folder.");
            }

            await next();
        });
    }

    analyzeDirectory(dirPath) {
        if (!fs.existsSync(dirPath)) return "⚠️ scripts/ folder not found.";

        const files = fs.readdirSync(dirPath).filter(f => f.endsWith('.js'));
        const graph = {};
        const fileContents = {};

        for (let file of files) {
            const fullPath = path.join(dirPath, file);
            const content = fs.readFileSync(fullPath, 'utf8');
            fileContents[file] = content;

            const deps = [];
            const regex = /require\(['"](.+?)['"]\)|import .* from ['"](.+?)['"]/g;
            let match;
            while ((match = regex.exec(content)) !== null) {
                const depPath = match[1] || match[2];
                let dep = depPath;
                if (!dep.endsWith('.js')) dep += '.js';
                if (dep.startsWith('./')) dep = dep.replace('./', '');
                deps.push(dep);
            }

            graph[file] = deps.filter(d => files.includes(d));
        }

        const loadOrder = this.topoSort(graph);
        const explanation = loadOrder.map((f, i) => `${i + 1}. ${f}`).join('\n');
        return `📊 Suggested Load Order:\n${explanation}`;
    }

    topoSort(graph) {
        const visited = new Set();
        const stack = [];

        const visit = (node) => {
            if (!visited.has(node)) {
                visited.add(node);
                (graph[node] || []).forEach(dep => visit(dep));
                stack.push(node);
            }
        };

        Object.keys(graph).forEach(visit);
        return stack.reverse();
    }
}

module.exports.ScriptAnalyzerBot = ScriptAnalyzerBot;
