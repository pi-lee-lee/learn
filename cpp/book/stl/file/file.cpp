#include <iostream>
#include <string>
#include <filesystem>
#include <fstream>


using namespace std;
using namespace filesystem;


int main(int arg, char* argv[]){
    create_directories("DDD");

    ofstream outf("DDD/myfile.txt");
    outf<<"eeee"<<"한글됨?"<<endl;
    outf.close();

    cout << " file in : \n";
    for(const directory_entry &entry : directory_iterator("DDD")){
        if(entry.is_regular_file()){
            cout << entry.path().filename() << endl;
        }
    }

    ifstream inf("DDD/myfile.txt");
    string line;
    
    while(getline(inf, line)){
        cout<<line<<endl;
    }

    inf.close();



    remove_all("DDD");
    return 0;
}