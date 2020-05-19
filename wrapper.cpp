#include <pybind11/pybind11.h>
#include <iostream>
#include <iomanip>
#include <cmath>

namespace py = pybind11;

class Solver{
  public:
    void solve(int n, py::list left, py::list right);
    double *X;
    int size;
    bool solved;
  
  private:
    bool ludist (int n, double ** A);
    bool lusolve (int n, double ** A, double * B);
};


bool Solver::ludist (int n, double ** A)
{
  int i, j, k;

  for( k = 0; k < n - 1; k++ )
  {
    if(fabs(A[k][k]) < 1e-12)
    {
      return false;
    }

    for(i = k + 1; i < n; i++)
    {
      A [i][k] /= A [k][k];
    }

    for(i = k + 1; i < n; i++)
    {
      for(j = k + 1; j < n; j++)
      {
        A[i][j] -= A[i][k] * A[k][j];
      }
    }
  
  }

  return true;
}


bool Solver::lusolve ( int n, double ** A, double * B)
{
  int i, j;
  double s;

  X[0] = B[0];

  for(i = 1; i < n; i++)
  {
    s = 0;

    for(j = 0; j < i; j++)
    {
      s += A[i][j] * X[j];
    }

    X[i] = B[i] - s;
  }

  if(fabs(A[n-1][n-1]) < 1e-12)
  {
    return false;
  }

  X[n-1] /= A[n-1][n-1];

  for(i = n - 2; i >= 0; i--)
  {
    s = 0;

    for(j = i + 1; j < n; j++) 
    {
      s += A [i][j] * X[j];
    }

    if( fabs ( A [ i ][ i ] ) < 1e-12 )
    {
      return false;
    }

    X[i] = (X[i] - s) / A[i][i];
  }

  return true;
}

void Solver::solve(int n, py::list left, py::list right) {
  this->size = n;
	double **A, *B;
	int i;
  solved = true;

	//std::cout << std::setprecision ( 4 ) << std::fixed;

	A = new double * [n];
	B = new double [n];
	X = new double [n];

	for( i = 0; i < n; i++ ) A [ i ] = new double [ n ];
    int counter = 0, counter1 = 0;
	for (auto item : left)
    {
        for(auto item2 : item)
        {
            A[counter][counter1] = atof(std::string(py::str(item2)).c_str());
            counter1 ++;
        }
        counter ++;
        counter1 = 0;
    }

    for (auto item : right)
    {
        B[counter1] = atof(std::string(py::str(item)).c_str());
        counter1 ++;
    }

	if(!ludist (n, A) || !lusolve (n, A, B))
	{
		//std::cout << "DZIELNIK ZERO\n";
    solved = false;
	}

	for( i = 0; i < n; i++ )
  {
    delete [ ] A [ i ];
  }
  delete [ ] A;
	delete [ ] B;

}

PYBIND11_MODULE(equations_solver, m) {
    // m.doc() = "pybind11 example plugin"; // Optional module docstring
    // m.def("solve", solve, "Method of solving systems of linear equations");
        py::class_<Solver>(m, "Solver")
        .def(py::init<>())
        .def("solve", &Solver::solve)
        .def("__repr__",
        [](const Solver &a) {
            std::string results = "";
            for(int i = 0; i < a.size; i++)
            {
              results += std::to_string(a.X[i]) + ":";
            }
            if(!a.solved){
              results = "false";
            }
            return results;
        }
    );
}