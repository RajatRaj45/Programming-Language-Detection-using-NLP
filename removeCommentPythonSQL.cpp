#include <iostream>
#include <filesystem>
#include <fstream>
using namespace std;
using ll=long long int;

namespace fs = filesystem;



// Function to process a single file
void processFile(const fs::path& inputFile, const fs::path& outputDir) {
    // Open input file for reading
    ifstream inFile(inputFile);
    if (!inFile.is_open()) {
        cerr << "Failed to open file: " << inputFile << endl;
        return;
    }

    // Create output file path
    fs::path outputFile = outputDir / (inputFile.filename().stem().string() + "_output.txt");

    // Open output file for writing
    ofstream outFile(outputFile);
    if (!outFile.is_open()) {
        cerr << "Failed to create output file: " << outputFile << endl;
        return;
    }

    // Process the input file
    // string line;
    // while (getline(inFile, line)) {
    //     // Process each line as needed
    //     // For demonstration, simply write the line to the output file
    //     outFile << line << endl;
    // }
    // *************************************************************************************************************

    string sourceCode = "";
    string line;
    while(getline(inFile,line)){
        for(ll i=0;i<line.size();i++){
            if(line[i]=='#'){
                line=line.substr(0, i);
                break;
            }
        }

        sourceCode = sourceCode + line + " ";
    }

    string newSourceCode="";
    // cout<<sourceCode<<"\n";
    // cout<<"******************************\n";

    for(ll i=0;i<sourceCode.size()-2;i++){
        if(sourceCode[i]=='"' && sourceCode[i+1]=='"' && sourceCode[i+2]=='"'){
            ll j=i+3;
            while(j<sourceCode.size()-2 && !(sourceCode[j]=='"' && sourceCode[j+1]=='"' && sourceCode[j+2]=='"')){
                j++;
            }
            i=j+2;
        }
        else{
            newSourceCode.push_back(sourceCode[i]);
        }
    }
    newSourceCode.push_back(sourceCode[sourceCode.size()-2]);

    // cout<<newSourceCode<<"\n";
    outFile << newSourceCode << endl;


    // ***********************************************************************************************************************



    cout << "Processed file: " << inputFile <<endl;
}

// Function to iterate over files in a directory
void processDirectory(const fs::path& inputDir, const fs::path& outputDir) {
    for (const auto& entry : fs::directory_iterator(inputDir)) {
        if (fs::is_regular_file(entry)) {
            processFile(entry.path(), outputDir);
        }
    }
}

int main() {
    // Input directory path
    fs::path inputDir = "/mnt/c/Users/hp/OneDrive/Desktop/VSCode/compilerDesign/fullDataset/SQL";

    // Output directory path
    fs::path outputDir = "/mnt/c/Users/hp/OneDrive/Desktop/VSCode/compilerDesign/outputCodes/SQL";

    // Check if input directory exists
    if (!fs::exists(inputDir) || !fs::is_directory(inputDir)) {
        cerr << "Input directory does not exist or is not a directory: " << inputDir << endl;
        return 1;
    }

    // Create output directory if it doesn't exist
    if (!fs::exists(outputDir)) {
        if (!fs::create_directories(outputDir)) {
            cerr << "Failed to create output directory: " << outputDir << endl;
            return 1;
        }
    }

    // Process files in the input directory
    processDirectory(inputDir, outputDir);

    return 0;
}